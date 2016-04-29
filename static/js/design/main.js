inputTextArr = []
selectedText = ""

$( document ).ready(function() {
	console.log( "ready!" );

	$("#fullpage").fullpage({
		// Scrolling
		'css3': true,
		'scrollingSpeed': 700,

		// Design
		'verticalCentered': false,
		'sectionsColor': ['#EEEDED', '#DCDCDC', '#EEEDED', '#DCDCDC'],

		// Accessibility
		keyboardScrolling: false,

		// Event
		onLeave: function(index, nextIndex, direction){
			progress_off(steps_ui[index-1]);
			progress_on(steps_ui[nextIndex-1]);
		}
	});

	// Setting
	$.fn.fullpage.setMouseWheelScrolling(false);
	$.fn.fullpage.setAllowScrolling(false);

	var nav = $("#design_nav");

	var step1_ui = [$("#step1_progress"), $("#step1_container")];
	var step2_ui = [$("#step2_progress"), $("#step2_container")];
	var step3_ui = [$("#step3_progress"), $("#step3_container")];
	var step4_ui = [$("#step4_progress"), $("#step4_container")];
	var steps_ui = [step1_ui, step2_ui, step3_ui, step4_ui];

	for (var i = 0; i < steps_ui.length; i++) {
		steps_ui[i][0].click(function(e){
			e.preventDefault();
			progressIndex = $(this).attr("tag");
			$.fn.fullpage.moveTo(progressIndex);
		});
	}

	var step1_plus_btn = $("#step1_image_plus");
	var step1_minus_btn = $("#step1_image_minus");
	
	step1_plus_btn.click(function(){
		$(this).focus();		
	});

	step1_minus_btn.click(function(){
		$(this).focus();
	});

	// init
	nav.click();
	progress_on(step1_ui);

	var scatchImages = $("#step1_scatch_images");
	scatchImages.imagepicker({
		show_label: true
	});

	// Step 1. Scatch
	
	var Step1 = new StepOne();

	var scatch_btn = $("#step1_scatch_btn");
	scatch_btn.click(function(){
		Step1.scatch();	
	});

	var step1_next_btn = $("#step1_next");
	step1_next_btn.click(function(){
		if (selectedText != "") {
			Step1.next();

			$.fn.fullpage.moveSectionDown();
		} else {
			alert("Scatch & Select!");
		}
	});

	// Step 2. Edit Detail

	var Step2 = new StepTwo();
	//Step2.progress();

	var step2_next_btn = $("#step2_next");
	step2_next_btn.click(function(){
		Step2.next();

		$.fn.fullpage.moveSectionDown();
	});

	// Step 3. Design

	var Step3 = new StepThree(step4_ui);
	//Step3.progress();

	var step3_next_btn = $("#step3_next");
	step3_next_btn.click(function(){
		Step3.next();

		$.fn.fullpage.moveSectionDown();
	});

	// Step 4. Similar Fashion

	var Step4 = new StepFour();
	//Step4.progress();

});

