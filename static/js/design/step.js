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
			imagePath = response.results;

			superResoluteNRImage(imagePath, function(response) {
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
		});
	}
}

StepOne.prototype.next = function() {

	var designedPath = this.designedPath
	
	superResoluteX2Image(selectedText, function(response) {
		Caman("#step2_image_canvas", designedPath + response.results, function () {
			this.render();
		});
	});

}

function StepTwo() {
	this.designedPath = "/static/designed/"
}

StepTwo.prototype.progress = function() {
	// ....
}

StepTwo.prototype.next = function() {
	var designedPath = this.designedPath
	
	var big_image = $("#step3_big_image");
	big_image.attr('src', designedPath + selectedText);

	var circle_image = $("#step3_circle_image");
	circle_image.attr('src', designedPath + selectedText);

	var patchCount = 25
	classifyGenderImage(selectedText, function(response) {
		var female = 0; var male = 0
		response.results.forEach(function(item, index) {
			female += item[0];
			male += item[1];
		});
		
		female = Math.round(female*4);
		male = Math.round(male*4);

		var femaleProgressBar = $("#classify_gender_female");
		femaleProgressBar.progressbar({
			value: female
		});
		var femaleProgressBarValue = femaleProgressBar.find(".ui-progressbar-value");
		femaleProgressBarValue.css({
			"background": '#C08080'
		});
		
		var maleProgressBar = $("#classify_gender_male");
		maleProgressBar.progressbar({
			value: male
		});
		var maleProgressBarValue = maleProgressBar.find(".ui-progressbar-value");
		maleProgressBarValue.css({
			"background": '#438C56'
		});
	});

//	classifyCategoryImage(selectedText, function(response) {
//		category = [0, 0, 0, 0, 0, 0];
//		response.results.forEach(function(item, index) {
//			for(var i=0; i<6; i++) {
//				category[i] += item[i];
//			}
//		});
//
//		category.forEach(function(item, index) {
//			category[index] = Math.round(item*4);
//		});
//
//		console.log(category);
//
//		var myChart = echarts.init(document.getElementById('echart_pie2'), theme);
//		myChart.setOption({
//		  tooltip: {
//			trigger: 'item',
//			formatter: "{a} <br/>{b} : {c} ({d}%)"
//		  },
//		  calculable: true,
//		  series: [{
//			name: 'Area Mode',
//			type: 'pie',
//			radius: [25, 90],
//			center: ['50%', 170],
//			roseType: 'area',
//			x: '50%',
//			max: 100,
//			sort: 'ascending',
//			data: [{
//			  value: category[0],
//			  name: 'Street'
//			}, {
//			  value: category[1],
//			  name: 'Casual'
//			}, {
//			  value: category[2],
//			  name: 'Sexy'
//			}, {
//			  value: category[3],
//			  name: 'Unique'
//			}, {
//			  value: category[4],
//			  name: 'Work wear'
//			}, {
//			  value: category[5],
//			  name: 'Classic'
//			}]
//		  }]
//		});
//	});

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


