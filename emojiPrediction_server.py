from flask import Flask,request,jsonify
import json
import json
import spacy
nlp = spacy.load("en_core_web_sm")


def modify_dataset(keys,unicode):
    with open("improved_dataset.json", "r") as read_file:
        dataset = json.load(read_file)
    # codepoint=input("Please enter the emoji(Unicode) you associate with the sentence")
    codepoint=unicode
    keys=list(keys)
    tempdict=dict()
    tempdict.update({'keywords':keys,'unicode':codepoint})
    dataset.insert(0,tempdict)
    with open("improved_dataset.json", "w") as read_file:
        json.dump(dataset, read_file)

def emoji_prediction(text):
    with open("improved_dataset.json", "r") as read_file:
        dataset = json.load(read_file)
    dataset_size=len(dataset)
    text=text.lower()#converting all text to lowercase
    doc=nlp(text)
    tokens=[token.text for token in doc if not token.is_stop]#removing stop words
    seperator=" "
    text=seperator.join(tokens)#created new string after removing stop words
    text.upper()
    doc=nlp(text)
    #lemmatization and removal of punctuation
    temp=[]
    for token in doc:
    # print(token.lemma_+"     "+token.pos_)
        if(token.lemma_!="-PRON-"):
            if(token.is_punct==False):
                if(token.pos_!="PROPN"):#removing proper nouns
                    temp.append(token.lemma_)

    text=seperator.join(temp)
    text=text.lower()#converting all text to lowercase
    doc=nlp(text)
    #creating keys from the text
    keys1=[]
    for token in doc:
        keys1.append(token.text)
    keys=set(keys1)#to remove multiple occurances
    
    key_size=len(keys)
    found=0
    foundindex=-1
    score=0
    maxscore=0
    
    seperator=" "
    for i in range (dataset_size):
        ttemp2=[]
        score=0
        temp3=seperator.join(dataset[i]["keywords"])
        doc4=nlp(temp3)
        for token in doc4:
            ttemp2.append(token.lemma_)#lemmatizing the keywords
        temp3=seperator.join(ttemp2)
        bag=temp3.split(" ")
        bagOfWords=set(bag)
        score=len(bagOfWords & keys)#finding no. of common keywords
        if(score>maxscore):
        #print(f"maxscore={maxscore}---score={score}---indexOfNewMax={i}")
        #print(bagOfWords)
            found=1
            foundindex=i
            maxscore=score

    if(found==1):
        unicode=dataset[foundindex]["unicode"]
        unicode=unicode.split()
        emoji=[]
        for x in unicode:
            temp='0x'+x[2:]
            emoji.append(temp)
    else:
        emoji=['0']
        unicode=['0']

    resultDict={
        "found":found,
        "foundindex":foundindex,
        "keys":list(keys),
        "unicode":unicode[0],
        "emoji":emoji[0],
    }
    return resultDict


app = Flask(__name__)

@app.route('/')
def index():
    return "Flask Server"

@app.route('/predict_emoji',methods=['POST'])
def predict():
    data=request.get_json()
    text=data['input']
    result=emoji_prediction(text)
    print(result)
    return jsonify(result)

@app.route('/modify_database',methods=["POST"])
def modify():
    data=request.get_json()
    keys=data['keys']
    unicode=data['unicode']
    modify_dataset(keys,unicode)
    print("done")
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)
    print("flask server running on port 5000")