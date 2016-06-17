inputTextArr = []
selectedText = ""

$( document ).ready(function() {
	console.log( "ready!" );
	
	$("#fullpage_design").fullpage({
		// Scrolling
		'css3': true,
		'scrollingSpeed': 700,

		// Design
		'verticalCentered': false,
		'sectionsColor': ['#EEEDED', '#DCDCDC', '#EEEDED', '#DCDCDC', '#EEEDED', '#DCDCDC'],

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


	var top10_ui = [$("#top10_progress"), $("#top10_container")];
	var collection_ui = [$("#collection_progress"), $("#collection_container")];
	var step1_ui = [$("#step1_progress"), $("#step1_container")];
	var step2_ui = [$("#step2_progress"), $("#step2_container")];
	var step3_ui = [$("#step3_progress"), $("#step3_container")];
	var step4_ui = [$("#step4_progress"), $("#step4_container")];
	var steps_ui = [top10_ui, collection_ui, step1_ui, step2_ui, step3_ui, step4_ui];

	for (var i = 0; i < steps_ui.length; i++) {
		steps_ui[i][0].click(function(e){
			e.preventDefault();
			progressIndex = $(this).attr("tag");
			$.fn.fullpage.moveTo(progressIndex);
		});
	}

	// Init
	var gallery_nav = $("#gallery_nav");
	var design_nav = $("#design_nav");

	design_nav.click();
	progress_on(step1_ui);
	$.fn.fullpage.moveTo(3);

	var scatchImages = $("#step1_scatch_images");
	scatchImages.imagepicker({
		show_label: true
	});

	// Top10

	var top10 = new Top10();
	top10.getList();

	// WordCloud
	
	var collection = new Collection();
	collection.wordcloud();

	// Step 1. Scatch
	
	var Step1 = new StepOne();

	var step1_input = $("#step1_input_text");
	step1_input.keypress(function(e) {
		if (e.which == 13) {
			// Enter
			Step1.scatch();
		}
	});

	var scatch_btn = $("#step1_scatch_btn");
	scatch_btn.click(function(){
		Step1.scatch();	
	});

	var step1_next_btn = $("#step1_next");
	step1_next_btn.click(function(){
		if (selectedText != "") {
			Step1.next();

			$.fn.fullpage.moveSectionDown();
			$(this).unbind();
		} else {
			alert("Scatch & Select!");
		}
	});

	var Step2 = new StepTwo();
	var Step3 = new StepThree(step4_ui);
	
	var step2_next_btn = $("#step2_next");
	step2_next_btn.click(function(){
		Step2.next();
		Step3.desginDetail();

		$.fn.fullpage.moveSectionDown();
		$(this).unbind();
	});

	var step3_next_btn = $("#step3_next");
	step3_next_btn.click(function(){
		Step3.next();

		$.fn.fullpage.moveSectionDown();
		$(this).unbind();
	});
	
});

