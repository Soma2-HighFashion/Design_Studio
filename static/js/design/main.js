function progress_ui(step) {
	progress = step[0]; container = step[1];

	var li = progress.parent()
	li.addClass("current-page");
	container.removeClass("hide");
}

$( document ).ready(function() {
	console.log( "ready!" );

	var nav = $("#design_nav");

	var step1_ui = [$("#step1_progress"), $("#step1_container")];
	var step2_ui = [$("#step2_progress"), $("#step2_container")];
	var step3_ui = [$("#step3_progress"), $("#step3_container")];
	var step4_ui = [$("#step4_progress"), $("#step4_container")];

	// init
	nav.click();
	progress_ui(step1_ui);

	var input_text_btn = $("#input_text_modal");
	input_text_modal.click();

	var Step1 = new StepOne(step2_ui);
	Step1.progress();

	var Step2 = new StepTwo(step3_ui);
	Step2.progress();

	var Step3 = new StepThree(step4_ui);
	Step3.progress();

	var Step4 = new StepFour();
	Step4.progress();

});

