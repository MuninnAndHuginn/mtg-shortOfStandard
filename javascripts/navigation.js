function setState(which){
	$("div.content").hide();
	var toShow = "div.content#" + which;
	
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

