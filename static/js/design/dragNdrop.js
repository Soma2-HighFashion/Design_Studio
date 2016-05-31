function initButton() {
	$("#step1_image_plus").removeClass('clicked');
	$("#step1_image_minus").removeClass('clicked');
}

var step1PlusBtn = $("#step1_image_plus");
step1PlusBtn.click(function(event) {

	$(this).toggleClass('clicked');

	function dropPlus( event, ui ) {
		var draggable = ui.draggable;
		
		$(this).hide("slow");
		$(draggable).hide("slow");
		
		var dragText = $(draggable).find("p").text();
		var dropText = $(this).find("p").text();

		$("#step1_scatch_images").children().each(function(index) {
			optionVal = $(this).val();
			if ((optionVal == dragText) || (optionVal == dropText)) {
				$(this).remove();
			}
		});

		textValue = dragText + " + " + dropText;
		var Step1 = new StepOne();
		Step1.scatch(textValue);

		initButton();
	}

	$(".image_picker_selector div").draggable( {
		cursor: 'move',
		containment: '.image_picker_selector',
		stack: '.image_picker_selector div',
		revert: true
	});
	
	$(".image_picker_selector div").droppable( {
		accept: '.image_picker_selector div',
		hoverClass: 'hovered',
		drop: dropPlus
	});

});

var step1MinusBtn = $("#step1_image_minus");
step1MinusBtn.click(function(event) {

	$(this).toggleClass('clicked');
	
	function dropMinus( event, ui ) {
		var draggable = ui.draggable;

		$(this).hide("slow");
		$(draggable).hide("slow");

		var dragText = $(draggable).find("p").text();
		var dropText = $(this).find("p").text();

		$("#step1_scatch_images").children().each(function(index) {
			optionVal = $(this).val();
			if ((optionVal == dragText) || (optionVal == dropText)) {
				$(this).remove();
			}
		});

		textValue = dragText + " - " + dropText;
		var Step1 = new StepOne();
		Step1.scatch(textValue);

		initButton();
	}

	$(".image_picker_selector div").draggable( {
		cursor: 'move',
		containment: '.image_picker_selector',
		stack: '.image_picker_selector div',
		revert: true
	});
	
	$(".image_picker_selector div").droppable( {
		accept: '.image_picker_selector div',
		hoverClass: 'hovered',
		drop: dropMinus
	});

});

