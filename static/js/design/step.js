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

}

StepOne.prototype.scatch = function() {

	var textValue = $("#step1_input_text").val();

	if (textValue == "") {
		alert("Insert Text!");
	} else if (inputTextArr.includes(textValue)) {
		alert("Duplicate Text!");
	} else {
		inputTextArr.push(textValue);
		generateImage('generator', '', function(response) {
			var scatchImages = $("#step1_scatch_images");
			scatchImages.append(
				'<option data-img-label="'+textValue+
				'"data-img-src="/static/generator/' + response.results + 
				'" data-img-label="Test" value="'+textValue+
				'"></option>');	
			scatchImages.imagepicker({
				show_label: true,
				clicked:function(){
					imagePath = $(this).find("option[value='" + $(this).val() + "']").data('img-src');
					selectedText = imagePath;
				}
			});
		});
	}
}

StepOne.prototype.next = function() {

	$(function () {

		var console = window.console || { log: function () {} },
			$alert = $('.docs-alert'),
			$message = $alert.find('.message'),
			showMessage = function (message, type) {
				$message.text(message);

				if (type) {
				  $message.addClass(type);
				}

				$alert.fadeIn();

				setTimeout(function () {
					$alert.fadeOut();
				}, 3000);
			};

		(function () {
			var $image = $('.img-container > img'),
				$dataX = $('#dataX'),
				$dataY = $('#dataY'),
				$dataHeight = $('#dataHeight'),
				$dataWidth = $('#dataWidth'),
				$dataRotate = $('#dataRotate'),
				options = {
					aspectRatio: 16 / 9,
					preview: '.img-preview',
					crop: function (data) {
						$dataX.val(Math.round(data.x));
						$dataY.val(Math.round(data.y));
						$dataHeight.val(Math.round(data.height));
						$dataWidth.val(Math.round(data.width));
						$dataRotate.val(Math.round(data.rotate));
					}
				};

		$image.on({
			'build.cropper': function (e) {
				console.log(e.type);
			},
			'built.cropper': function (e) {
				console.log(e.type);
			}
		}).cropper(options);


		// Methods
		$(document.body).on('click', '[data-method]', function () {
			var data = $(this).data(),
				$target,
				result;

			if (data.method) {
				data = $.extend({}, data); // Clone a new one

				if (typeof data.target !== 'undefined') {
					$target = $(data.target);

					if (typeof data.option === 'undefined') {
						try {
							data.option = JSON.parse($target.val());
						} catch (e) {
							console.log(e.message);
						}
					}
				}

				result = $image.cropper(data.method, data.option);

				if (data.method === 'getDataURL') {
					$('#getDataURLModal').modal().find('.modal-body').html('<img src="' + result + '">');
				}

				if ($.isPlainObject(result) && $target) {
					try {
						$target.val(JSON.stringify(result));
					} catch (e) {
						console.log(e.message);
					}
				}

			}
		}).on('keydown', function (e) {

			switch (e.which) {
				case 37:
					e.preventDefault();
					$image.cropper('move', -1, 0);
					break;

				case 38:
					e.preventDefault();
					$image.cropper('move', 0, -1);
					break;

				case 39:
					e.preventDefault();
					$image.cropper('move', 1, 0);
					break;

				case 40:
					e.preventDefault();
					$image.cropper('move', 0, 1);
					break;
			}

		});


		// Import image
		var $inputImage = $('#inputImage'),
			URL = window.URL || window.webkitURL,
			blobURL;

		if (URL) {
			$inputImage.change(function () {
				var files = this.files,
					file;

				if (files && files.length) {
					file = files[0];

					if (/^image\/\w+$/.test(file.type)) {
						blobURL = URL.createObjectURL(file);
						$image.one('built.cropper', function () {
							URL.revokeObjectURL(blobURL); // Revoke when load complete
						}).cropper('reset', true).cropper('replace', blobURL);
						$inputImage.val('');
					} else {
						showMessage('Please choose an image file.');
					}
				}

			});
		} else {
			$inputImage.parent().remove();
		}


		// Options
		$('.docs-options :checkbox').on('change', function () {
			var $this = $(this);

			options[$this.val()] = $this.prop('checked');
			$image.cropper('destroy').cropper(options);
		});


		// Tooltips
		$('[data-toggle="tooltip"]').tooltip();

		}());

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


