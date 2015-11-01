function setState(which){
	$("div.content").hide();
	var toShow = "div.content#" + which;
	var toLoad = "div.content#" + which + " div.extern";
	var loadingUrl = "./externs/"+ which + ".html";

	$(toLoad).load(loadingUrl);
	$(toShow).show();
};

$(document).ready(function(){
	setState("Home");
	
	$("div#menu li").each(function(index) {
		$(this).click(function() {
			setState($(this).text());
		});
	});
});

