// $('#login-button').click(function (event) {
// 	event.preventDefault();
// 	$('form').fadeOut(500);
// 	$('.wrapper').addClass('form-success');
// });
function login() {
	document.getElementById("warnword").innerHTML = "";
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;
	var info = { "name": username, "passwd": password };
	$.ajax({
		url: "php/login.php",
		type: "POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			if (data.message == 'success') {
				$('form').fadeOut(500);
				$('.wrapper').addClass('form-success');

				var url = "main.html";
				var newurl = url.concat("?", "username=", username);

				setTimeout(function () { window.location.href = newurl; }, 2000);
			}
			else if (data.message == 'wrong_pwd') {
				document.getElementById("warnword").innerHTML = "系统提示：密码错误";
			}
			else {
				document.getElementById("warnword").innerHTML = "系统提示：用户名不存在";
			}
		},
		error: function (err) {
			console.log(err);
			console.log("服务器未响应");
		}
	});
}

function signin() {
	var username = document.getElementById("username").value;
	var mailbox = document.getElementById("mailbox").value;
	var password = document.getElementById("password").value;
	var cheakpwd = document.getElementById("cheakpwd").value;
	var sex = document.getElementById("sex").value;
	var birth = document.getElementById("birth").value;
	var place = document.getElementById("place").value;
	if (username == "" || mailbox == "" || password == "" || cheakpwd == "" || sex == "" || birth == "" || place == "") {
		//window.alert("请填写所有表格");
		document.getElementById("warnword").innerHTML = "系统提示：请填写全部信息";
		return;
	}
	var myReg = /^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
	if (!myReg.test(mailbox)) {
		document.getElementById("warnword").innerHTML = "系统提示：邮箱格式不正确";
		return;
	}
	if (password != cheakpwd) {
		document.getElementById("warnword").innerHTML = "系统提示：前后密码不一致";
		return;
	}
	if (sex != "男" && sex != "女") {
		document.getElementById("warnword").innerHTML = "系统提示：性别只限填“男”或“女”";
		return;
	}
	var info = { "name": username, "passwd": password, "mail": mailbox, "sex": sex, "birth": birth, "place": place };
	$.ajax({
		url: "php/signin.php",
		type: "POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			if (data.message == "success")
			{
				document.getElementById("warnword").innerHTML="系统提示：注册成功，3秒后将返回到登录界面";
				setTimeout(function () { window.location.href = "index.html"; }, 3000);
			}
			else if(data.message=="user_exsit")document.getElementById("warnword").innerHTML="系统提示：用户名已存在";
			else if(data.message=="mailbox_exsit")document.getElementById("warnword").innerHTML="系统提示：邮箱已注册";
			else document.getElementById("warnword").innerHTML="系统提示：注册失败";
		},
		error: function (err) {
			console.log("服务器未响应");
			console.log(err);
		}
	});
}

function findpwd() {
	var username = document.getElementById("username").value;
	var mailbox = document.getElementById("mailbox").value;
	var info = { "name": username, "mailbox": mailbox };
	$.ajax({
		url: "php/forgetpwd.php",
		type: "POST",
		dataType: 'json',
		data: info,
		success: function (data) {
			console.log(data);
			if (data.state == "right") {
				document.getElementById("warnword").innerHTML = "系统提示：你的密码为：" + data.message;
			}
			else if (data.state == "namewrong") {
				document.getElementById("warnword").innerHTML = "系统提示：不存在该用户";
			}
			else {
				document.getElementById("warnword").innerHTML = "系统提示：邮箱错误";
			}
		},
		error: function (err) {
			console.log(err);
			console.log("服务器未响应");
		}
	});
}