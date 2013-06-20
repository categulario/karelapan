$(document).ready(function(){
	$("#grupo").change(function(event){
		if($(this).val() == 3){
			$(".solo-olimpicos").removeClass('hidden');
		} else {
			$(".solo-olimpicos").addClass('hidden');
		}
	});
});
