//取得当前URL，跳转时加上用户名
function function0(params) {
	var username=getQueryVariable("username");
	var url=params+"?"+"username="+username;
	console.log(url);
	window.location.href=url;
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