$(function () {
	var username = getQueryVariable("username");
	document.getElementById("getusername").innerHTML = username;
	document.getElementById("infoname").innerHTML = "用户名：" + username;
	getinfo();
	load_my_article();
	load_my_picture();
})

function getQueryVariable(variable) {
	var query = window.location.search.substring(1);
	var vars = query.split("&");
	for (var i = 0; i < vars.length; i++) {
		var pair = vars[i].split("=");
		if (pair[0] == variable) { return pair[1]; }
	}
	return (false);
}

function hideall() {
	//document.getElementById("one").style.display="none";
	document.getElementById("two").style.display = "none";
	document.getElementById("three").style.display = "none";
	document.getElementById("four").style.display = "none";
	document.getElementById("five").style.display = "none";
}

function show_div(param) {
	hideall();
	document.getElementById(param).style.display = "";
}

function getinfo() {
	var username = getQueryVariable("username");
	var info = { "username": username };
	$.ajax({
		url: "php/userinfo.php",
		type: "POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			//console.log(data);
			document.getElementById("infomail").innerHTML = "邮箱：" + data.mail;
			document.getElementById("infosex").innerHTML = "性别：" + data.sex;
			document.getElementById("infobirth").innerHTML = "出生日期：" + data.birth;
			document.getElementById("infoplace").innerHTML = "所在城市：" + data.place;
			document.getElementById("real_head_picture1").setAttribute("src",data.path);
		},
		error: function (err) {
			console.log(err);
			window.alert("服务器未响应");
		}
	});
}

function change_password() {
	var username = getQueryVariable("username");
	var oldpwd = document.getElementById("oldpwd").value;
	var newpwd = document.getElementById("newpwd").value;
	var checkpwd = document.getElementById("checkpwd").value;
	if (newpwd != checkpwd) {
		window.alert("新密码前后不一致");
		return;
	}
	var info = { "username": username, "oldpwd": oldpwd, "newpwd": newpwd };
	$.ajax({
		url: "php/changepwd.php",
		type: "POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			window.alert(data.message);
			if (data.message == "密码修改成功") {
				location.reload();
			}
		},
		error: function (err) {
			console.log(err);
			window.alert("服务器未响应");
		}
	});
}


function checkImageType(filename) {
	var index = filename.lastIndexOf(".");
	var ext = filename.substring(index + 1, filename.length);
	var types = ["jpg", "bmp", "jpeg", "png"];
	for (var key in types) {
		console.log(ext.toLowerCase())
		if (types[key] === ext.toLowerCase()) {
			return true;
		}
	}
	return false;
}


function change_picture() {
	var username = getQueryVariable("username");
	document.getElementById("change_picture_name").value=username;
    var options = { 
        type: 'POST',
        url: 'php/changephoto.php',
        success:function(data){
            if(data.message=='success')
            {
				window.alert("头像修改成功");
				window.location.reload();
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

     $("#head_picture").submit(function(){ 
         $(this).ajaxSubmit(options);
         return false;   //防止表单自动提交
     });

    $("#head_picture").ajaxSubmit(options);
}

function logout() {
	url = "index.html";
	window.location.href = url;
}

function load_my_article()
{
	var username = getQueryVariable("username");
	var info={"username":username};
	$.ajax({
		url:"php/personal_center_article.php",
		type:"POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			if(data!=null)load_article(data);
		},
		error: function (err) {
			console.log(err);
			window.alert("服务器未响应");
		}
	})
}

function load_article(parm)
{
	var sourceNode = document.getElementById("my_article-0"); // 获得被克隆的节点对象
	var j = 0;
	for (var i = parm.length; i >= 1; i--) {
			var clonedNode = sourceNode.cloneNode(true); // 克隆节点 
			clonedNode.setAttribute("id", "my_article-" + i); // 修改一下id 值，避免id 重复 

			clonedNode.style.display = "";
			var iid = "my_article-" + i;

			sourceNode.parentNode.appendChild(clonedNode); // 在父节点插入克隆的节点 

			
			document.getElementById(iid).getElementsByClassName("my_article_id")[0].innerHTML ="编号"+ parm[j].articleid;
			document.getElementById(iid).getElementsByClassName("my_article_name")[0].innerHTML = parm[j].title;
			document.getElementById(iid).getElementsByClassName("my_article_comment")[0].innerHTML =  "评论数："+parm[j].comment_num;
			document.getElementById(iid).getElementsByClassName("my_article_time")[0].innerHTML = parm[j].uptime;
			document.getElementById(iid).getElementsByClassName("my_article_pic")[0].setAttribute("src",parm[j].path);
			j++;
	}
}

function load_my_picture()
{
	var username = getQueryVariable("username");
	var info={"username":username};
	$.ajax({
		url:"php/personal_center_picture.php",
		type:"POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			//console.log(data);
			if(data!=null)load_picture(data);
		},
		error: function (err) {
			console.log(err);
			window.alert("服务器未响应");
		}
	})
}

function load_picture(parm)
{
	var sourceNode = document.getElementById("hispic-0"); // 获得被克隆的节点对象
	var j = 0;
	for (var i = parm.length; i >= 1; i--) {
			var clonedNode = sourceNode.cloneNode(true); // 克隆节点 
			clonedNode.setAttribute("id", "hispic-" + i); // 修改一下id 值，避免id 重复 

			clonedNode.style.display = "";
			var iid = "hispic-" + i;

			sourceNode.parentNode.appendChild(clonedNode); // 在父节点插入克隆的节点 
			
            //document.getElementById(iid).getElementsByClassName("picid")[0].innerHTML=parm[j].picid;
			document.getElementById(iid).getElementsByClassName("detect_result")[0].innerHTML 
			="编号："+parm[j].picid+"<br>"+ parm[j].uptime+"<br>"+"患青光眼的概率："+parm[j].prob+"<br>"+"VCDR："+parm[j].vcdr+"<br>"+"HCDR："+parm[j].hcdr;
			document.getElementById(iid).getElementsByClassName("gon_pic")[0].setAttribute("src",parm[j].path);
			j++;
	}
}

function change_head_picture()
{
	document.getElementById("userphoto").click();
}