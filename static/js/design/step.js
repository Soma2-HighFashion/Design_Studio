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

function StepOne() {
	this.generatorPath = "/static/generator/"
	this.designedPath = "/static/designed/"
}

StepOne.prototype.scatch = function() {

	var textValue = $("#step1_input_text").val();
	var generatorPath = this.generatorPath

	if (textValue == "") {
		alert("Insert Text!");
	} else if (inputTextArr.includes(textValue)) {
		alert("Duplicate Text!");
	} else {
		inputTextArr.push(textValue);
		generateImage(function(response) {
			var scatchImages = $("#step1_scatch_images");
			scatchImages.append(
				'<option data-img-label="'+textValue+
				'"data-img-src="' + generatorPath + response.results + 
				'" data-img-label="Test" value="'+textValue+
				'" data-img-uid="' + response.results +
				'"></option>');	
			scatchImages.imagepicker({
				show_label: true,
				clicked:function(){
					imagePath = $(this).find("option[value='" + $(this).val() + "']").data('img-uid');
					selectedText = imagePath;
				}
			});

			$(".image_picker_selector img").width("60");
		});
	}
}

StepOne.prototype.next = function() {

	var designedPath = this.designedPath
	
	superResoluteImage(selectedText, function(response) {
//		Caman("#step2_image_canvas", designedPath + response.results, function () {
//			this.render();
//		});
	});

}

function StepTwo() {

}

StepTwo.prototype.progress = function() {
	// ....
}

StepTwo.prototype.next = function() {
	var big_image = $("#step3_big_image");
	big_image.attr('src', selectedText);

	var circle_image = $("#step3_circle_image");
	circle_image.attr('src', selectedText);
}

function StepThree(nextStep) {

}

StepThree.prototype.progress = function() {
	// ....
}

StepThree.prototype.next = function() {

}

function StepFour(nextStep) {
	
}

StepFour.prototype.progress = function() {
	// ....
}


