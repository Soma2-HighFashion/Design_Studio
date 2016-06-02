ctxPath = "" 

function generateImage(params, uiCallBackFunc) {
	commonAjaxFunction("generator?text=" + params, uiCallBackFunc);
}

function superResoluteX2Image(params, uiCallBackFunc) {
	commonAjaxFunction("super_resolution_x2?input=" + params, uiCallBackFunc);
}

function superResoluteNRImage(params, uiCallBackFunc) {
	commonAjaxFunction("super_resolution_nr?input=" + params, uiCallBackFunc);
}

function classifyGenderImage(params, uiCallBackFunc) {
	commonAjaxFunction("classify_gender?input=" + params, uiCallBackFunc);
}

function classifyCategoryImage(params, uiCallBackFunc) {
	commonAjaxFunction("classify_category?input=" + params, uiCallBackFunc);
}

function commonAjaxFunction(urlStr, callBack, callbackParam) {

	var callUrl = ctxPath + urlStr;

	$.ajax({
		type : "GET",
		url : callUrl,
		contentType : 'application/json',

		success : function(response) {
			callBack(response, callbackParam);
		},
		error : function() {
			alert("오류가 발생하였습니다. 다시 시도해주세요.");	
		},

	});
}
