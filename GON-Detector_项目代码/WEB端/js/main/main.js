jQuery(document).ready(function($){
	//open the lateral panel
	$('.cd-btn').on('click', function(event){
		event.preventDefault();
		$('.cd-panel').addClass('is-visible');
	});
	//clode the lateral panel
	$('.cd-panel').on('click', function(event){
		if( $(event.target).is('.cd-panel') || $(event.target).is('.cd-panel-close') ) { 
			$('.cd-panel').removeClass('is-visible');
			event.preventDefault();
		}
	});
	
	var username=getQueryVariable("username");
	var welcome="欢迎你，"+username+"!";
	document.getElementById("welcome").innerHTML = welcome;
});

/*function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

function function0(params) {
	var username=getQueryVariable("username");
	var url=params+"?"+"username="+username;
	console.log(url);
	window.location.href=url;
}*/


$("#aaa").on('hidden.bs.modal', function () {
    console.log("summer");
    var videopause=document.getElementById("bbb");
    videopause.pause();
})