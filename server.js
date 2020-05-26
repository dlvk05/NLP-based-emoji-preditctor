var express= require("express"),
    app=express(),
    bodyParser = require("body-parser"),
    request = require('request-promise');

app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

var found=-1;
var returndata;
// ROUTES
app.get("/",(req,res)=>{
    res.render('home');
});

app.post("/home", async (req,res)=>{
    var data={
        "input":req.body.input
    };
    var options={
        method:"POST",
        uri:"http://localhost:5000/predict_emoji",
        body:data,
        json:true//automatically stringifies the body to JSON
    };
    var sendrequest = await request(options)
    .then(function(parsedBody){
        console.log(parsedBody);//parsedBody contains the data sent back from the Flask server
        returndata=parsedBody;
    })
    .catch(function(err){
        console.log(err);
    });

    if(returndata.found==1){
        returndata.redirect='false';
        res.send(returndata);
    }else{
        console.log("not Found logged from /home");
        returndata.redirect='true';
        returndata.redirectURL='/notFound';
        res.send(returndata);
        // res.redirect("/notFound");
    }
});


app.get("/notFound",(req,res)=>{
    console.log("/not found called");
    res.render('notFound');
});

app.post("/notfound",async (req,res)=>{

    var data={
        "keys":returndata.keys,
        // "unicode":req.body.unicode
        "unicode":req.body.emojiInput
    };

    console.log(data);

    var options={
        method:"POST",
        uri:"http://localhost:5000/modify_database",
        body:data,
        json:true//automatically stringifies the body to JSON
    };

    var sendrequest = await request(options)
    .then(function(parsedBody){
        console.log(parsedBody);//parsedBody contains the data sent back from the Flask server
    })
    .catch(function(err){
        console.log(err);
    });
    res.redirect('/');
});

app.listen(3000,()=>{
    console.log("server listening on port 3000");
});