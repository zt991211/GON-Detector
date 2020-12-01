jQuery(document).ready(function ($) {
    var username = getQueryVariable("username");
    document.getElementById("username").value = username;
    var welcome="欢迎你，"+username+"!";
	document.getElementById("welcome").innerHTML = welcome;
});

function uppic() {
    var options = {
        type: 'POST',
        url: 'php/save_picture.php',
        beforeSend: function() {
            document.getElementById("simple_data_buttom").style.display="";
          document.getElementById("loading").style.display="";  
        },
        success:function(data){
            if(data.message=='success')
            {
                    var v3_result=call_V3predict_model(data);
                    var cdr_result=call_CDRpredict_model(data);
                    document.getElementById("result").style.display="";                  
                    update_eyepic_result(v3_result,cdr_result,data.row_number); 
                    document.getElementById("loading").style.display="none";        
            }            
        },  
        dataType: 'json',
        error : function(xhr, status, err) {		
            alert("操作失败");
            console.log(xhr);
        },
        resetForm: false,
        clearForm: false
    }; 

     $("#dec_up_picture").submit(function(){ 
         $(this).ajaxSubmit(options);
         return false;   //防止表单自动提交
     });

     //$("#dec_up_picture").submit();
    $("#dec_up_picture").ajaxSubmit(options);
    //$("#dec_up_picture").ajaxForm(options);
    //$("#dec_up_picture").submit();
}

function call_CDRpredict_model(data)
{
    var username=data.username;
    var imgname=data.filename;
    target_url="http://47.113.114.73:5000/CDRpredict/"+username+"/"+imgname;
    var return_value;
    $.ajax({
        url: target_url,
        type: "GET",
        dataType: 'json',
        async:false,//这里选择异步为false，那么这个程序执行到这里的时候会暂停，等待数据加载完成后才继续执行(这样才能得到返回值)
        success: function (ddata) {
                document.getElementById("gon_hcdr").innerHTML="HCDR（水平杯盘比）："+ddata.HCDR;
                document.getElementById("gon_vcdr").innerHTML="VCDR（垂直杯盘比）："+ddata.VCDR;
                return_value=ddata;
        },
        error: function (err) {
                window.alert("服务器未响应");
                console.log(err);
        }
});
return return_value;
}

function call_V3predict_model(data)
{
    var username=data.username;
    var imgname=data.filename;
    target_url="http://47.113.114.73:5000/V3predict/"+username+"/"+imgname;
    var return_value;
    $.ajax({
        url: target_url,
        type: "GET",
        dataType: 'json',
        async:false,//这里选择异步为false，那么这个程序执行到这里的时候会暂停，等待数据加载完成后才继续执行
        success: function (ddata) {
                document.getElementById("gon_probability").innerHTML="患青光眼的概率："+ddata.PROB+"%";
                return_value=ddata;
        },
        error: function (err) {
                window.alert("服务器未响应");
                console.log(err);
        }
});
return return_value;
}

function preview(file) {
    var prevDiv = document.getElementById('preview');
    if (file.files && file.files[0]) {
        var reader = new FileReader();
        reader.onload = function (evt) {
            prevDiv.innerHTML = '<img src="' + evt.target.result + '" />';
            //console.log(evt.target.result);
        }
        reader.readAsDataURL(file.files[0]);
    } else {
        prevDiv.innerHTML = '<div class="img" style="filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale,src=\'' + file.value + '\'"></div>';
    }
}

function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) { return pair[1]; }
    }
    return (false);
}

function update_eyepic_result(v3_result,cdr_result,row_number)
{
    var info={"prob":v3_result.PROB,"vcdr":cdr_result.VCDR,"hcdr":cdr_result.HCDR,"row_number":row_number};
      $.ajax({
      url:"php/update_eyepic_result.php",
      type: "POST",
      dataType:'json',
      data:info,
      success: function(data){
        if(data.message=='success')
        {
            console.log("检测结果已保存至数据库"); 
        }    
      },
      error: function(err) {
        console.log(err);
      }
  });
}