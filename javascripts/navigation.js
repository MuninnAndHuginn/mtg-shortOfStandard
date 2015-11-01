function setState(which){
	$("section").hide();
	var toShow = "section#" + which;
	
	$(toShow).show();
};

$(document).ready(function(){
	setState("main");
	
	$("div#menu li").each(function(index) {
		$(this).click(function() {
			setState($(this).text());
		});
	});
});

