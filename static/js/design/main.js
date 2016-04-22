function progress_on(step) {
	progress = step[0]; container = step[1];

	var li = progress.parent()
	li.addClass("current-page");
}

function progress_off(step) {
	progress = step[0]; container = step[1];

	var li = progress.parent()
	li.removeClass("current-page");
}

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
		steps_ui[i][0].click(function(i){
			alert("test" + (i+1));
			$.fn.fullpage.moveTo(3);
		});
	}

	// init
	nav.click();
	progress_on(step1_ui);

	var scatch_btn = $("#step1_scatch_btn");
	scatch_btn.click(function(){
		$("#step1_scatch_images").append('<img src="http://img.hiphoper.com/images/lweb/file/street/thumb-32158264_Do18mlRr_2_162x253.jpg" width=128 height=128 style="margin: 3px;">');

		var images = $("#step1_scatch_images img");
		images.unbind('click');
		images.click(function(){
			$.fn.fullpage.moveSectionDown();
		});
	});

	var Step1 = new StepOne(step2_ui);
	Step1.progress();

	var Step2 = new StepTwo(step3_ui);
	//Step2.progress();

	var Step3 = new StepThree(step4_ui);
	//Step3.progress();

	var Step4 = new StepFour();
	//Step4.progress();

});

