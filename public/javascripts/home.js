$(function(){
    var $input=$('#input');
    var $resultTemplate=$('#emojiTemp').html();

    function spitOut(result){
        var $div=$('#emoji');
        $div.empty();
        var display=String.fromCodePoint(result.emoji);
        console.log(display);
        result.emoji=display;
        $div.append(Mustache.render($resultTemplate,result));
        console.log(result.emoji);
    }

    $('#sendInput').on('click',function(){
        var load=$('#loading');
        load.show();//show searching
        var dataTOSend={
            input:$input.val()
        };
        console.log(dataTOSend);
        $.ajax({
            type:'POST',
            url:'/home',
            data:dataTOSend,
            success:function(result){
                if(result.redirect=='false'){
                    console.log('here');
                    load.hide();//hide searching
                    spitOut(result);
                    $('#emojiModal').modal('show');
                    $('#copyTOclipboard').on('click',function(){
                        console.log('copy called');
                        $here=$('#here');
                        var emo=$here.text();
                        var $input=$(".copyfrom");
                        $input.value=emo;
                        $input.select();
                        document.execCommand("copy");
                        console.log(emo);
                        // $here.focus();
                        // $here.select();
                        // document.execCommand('copy');
                        alert('copied');
                    });
                }else{
                    window.location.href=result.redirectURL;
                }
                
            },
            error:function(){
                alert('error');
            }
        });
    });
});