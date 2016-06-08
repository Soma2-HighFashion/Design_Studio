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

predGender = [];
predCategory = [];
imgHistory = "0";
textHistory = "0";

function splitUid(path) {
	return path.split(".")[0];
}

function StepOne() {
	this.generatorPath = "/static/generator/"
	this.designedPath = "/static/designed/"
}

StepOne.prototype.scatch = function(inputText) {	

	var textValue = ""

	if (inputText == undefined) {
		textValue = $("#step1_input_text").val();
	} else {
		textValue = inputText;
	}

	var generatorPath = this.generatorPath;

	if (textValue == "") {
		alert("Insert Text!");
	} else if (inputTextArr.includes(textValue)) {
		alert("Duplicate Text!");
	} else {
		generateImage(textValue, function(response) {
			inputTextArr.push(textValue);
			imagePath = response.results;
			predGender = response.gender;
			predCategory = response.category;

			superResoluteNRImage(imagePath, function(response) {
				var scatchImages = $("#step1_scatch_images");
				scatchImages.append(
					'<option data-img-label="' + textValue +
					'"data-img-src="' + generatorPath + response.results + 
					'" data-img-label="Test" value="' + textValue +
					'" data-img-uid="' + response.results +
					'" data-img-gender="' + predGender +
					'" data-img-category="' + predCategory +
					'" data-img-history="' + splitUid(response.results)+
					'"></option>');	
				scatchImages.imagepicker({
					show_label: true,
					clicked:function(){
						imagePath = $(this).find("option[value='" + $(this).val() + "']").data('img-uid');
						selectedText = imagePath;
						imageHistory = $(this).find("option[value='" + $(this).val() + "']").data('img-history');
						imgHistory = imageHistory;

					}
				});
				$(".image_picker_selector img").width("50");
			});

			imageHandler(
				"",
				"POST",
				{
					"uid" : splitUid(imagePath),
					"gender" : predGender.toString(),
					"category" : predCategory.toString(),
					"text" : encodeURIComponent(textValue)
				},
				function(response) {
					image = response;
				}
			);

		});
	}
}

StepOne.prototype.next = function() {

	if (imgHistory == "0") {
		imgHistory = splitUid(imagePath);
	}

	designHandler(
		"",
		"POST",
		{
			"uid": splitUid(imagePath),
			"history_uid": imgHistory,
			"history_text": encodeURIComponent(textHistory),
			"filterd": false,
			"like": 0
		},
		function(response) {
			design = response;
		}
	);

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

	ratio = 100;

	var femaleProgressBar = $("#classify_gender_female");
	femaleProgressBar.progressbar({
		value: predGender[0] * ratio
	});
	var femaleProgressBarValue = femaleProgressBar.find(".ui-progressbar-value");
	femaleProgressBarValue.css({
		"background": '#C08080'
	});
	
	var maleProgressBar = $("#classify_gender_male");
	maleProgressBar.progressbar({
		value: predGender[1] * ratio
	});
	var maleProgressBarValue = maleProgressBar.find(".ui-progressbar-value");
	maleProgressBarValue.css({
		"background": '#438C56'
	});

	var maxValue = Math.max.apply(null, predCategory);
	var myChart = echarts.init(document.getElementById('analysis_raidor_chart'), theme);
	myChart.setOption({
	  tooltip: {
		trigger: 'item',
		formatter: "{a} <br/>{b} : {c} ({d}%)"
	  },
	  calculable: true,
	  polar : [
		{
		  indicator : [
			{text : 'Street', max  : maxValue},
			{text : 'Casual', max  : maxValue},
			{text : 'Classic', max  : maxValue},
			{text : 'Unique', max  : maxValue},
			{text : 'Sexy', max  : maxValue}
		  ],
		  radius : 130
		}
	  ],
	  series: [{
		name: 'Area Mode',
		type: 'radar',
		data: [
		  {
			value : predCategory,
			name : "category"
		  }
		]
	  }]
	});
}

function StepThree(nextStep) {

}

StepThree.prototype.progress = function() {
	// ....
}

StepThree.prototype.next = function() {
	searchNeighbors(selectedText, function(response) {

		var target = $("#similar-fashions");
		target.text("");

		var tagStr = "";
		var simImages = response.results;
		simImages.forEach(function(item, index) {
			tagStr += '<div class="col-md-2">';
			tagStr += '  <div class="thumbnail">';
			tagStr += '    <div class="image view view-first">';
			tagStr += '      <img style="display: block; margin: 0 auto;" src="static/designed/' + item.image + '" alt="image" />';
			tagStr += '      <div class="mask">';
			tagStr += '        <div class="tools tools-bottom">';
			tagStr += '          <p>'+ decodeURIComponent(item.text) +'</p>';
			tagStr += '        </div>';
			tagStr += '      </div>';
			tagStr += '    </div>';
			tagStr += '  </div>';
			tagStr += '</div>';
		});
		target.html(tagStr);
	});
}

function StepFour(nextStep) {
	
}

StepFour.prototype.progress = function() {
	// ....
}


