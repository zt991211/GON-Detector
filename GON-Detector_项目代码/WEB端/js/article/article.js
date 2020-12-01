jQuery(document).ready(function($){
	var username=getQueryVariable("username");
	var fwelcome="你好，"+username+"!";
    document.getElementById("fwelcome").innerHTML = fwelcome;

    var writer=getQueryVariable("writer");
    var num=getQueryVariable("num");
    var info={"name":writer,"num":num};


    $.ajax({
        url: 'php/load_markdown.php',
        type: 'POST',
        dataType: 'json',
        data:info,
        success:function(data){
            console.log(data.path);
            var converter = new Markdown.Converter();
            var htm = converter.makeHtml(data.message);
            $('#mdpassage').html(htm);
            document.getElementById("article_picture").setAttribute("src",data.path);
        }
    });

    $.ajax({
        url: 'php/load_comment.php',
        type: 'POST',
        dataType: 'json',
        data:info,
        success:function(data){
            //console.log(data);
            if(data!=null)
            commentload(data);
        },
        error: function(err) {
            window.alert("服务器未响应");
            console.log(err);
        }
    });

});

function commentload(parm)
{
    document.getElementsByClassName("commentnum")[0].innerHTML=parm.length+" 评论";
        var sourceNode = document.getElementById("comment-0"); // 获得被克隆的节点对象 
        for (var i = 1; i <= parm.length; i++) 
        { 
                var clonedNode = sourceNode.cloneNode(true); // 克隆节点 
                clonedNode.setAttribute("id", "comment-" + i); // 修改一下id 值，避免id 重复 

                clonedNode.style.display="";
                var iid="comment-" + i;

                sourceNode.parentNode.appendChild(clonedNode); // 在父节点插入克隆的节点 

                document.getElementById(iid).getElementsByClassName("author-name")[0].innerHTML=parm[i-1].commenter;
                document.getElementById(iid).getElementsByClassName("meta")[0].innerHTML=parm[i-1].uptime;
                document.getElementById(iid).getElementsByClassName("ccomment")[0].innerHTML=parm[i-1].comment;
                document.getElementById(iid).getElementsByClassName("avatar")[0].setAttribute("src",parm[i-1].pic);
                }
}

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

function upComment()
{
    var comment=document.getElementById("comment").value;
    var commenter=getQueryVariable("username");
    var mydate=new Date;
    var uptime=mydate.toLocaleString();
    var articlenum=getQueryVariable("num");
    var info={"commenter":commenter,"comment":comment,"uptime":uptime,"articlenum":articlenum};
    $.ajax({
      url: "php/comment.php",
      type: "POST",
      dataType:'json',
      data:info,
      success: function(data){
              window.alert(data.message);
              window.location.reload();       
      },
      error: function(err) {
          window.alert("服务器未响应");
          console.log(err);
      }
  });

}

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}