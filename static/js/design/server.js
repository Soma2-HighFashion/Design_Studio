ctxPath = "" 

function generateImage(uiCallBackFunc) {
	commonAjaxFunction("generator", uiCallBackFunc);
}

function superResoluteImage(params, uiCallBackFunc) {
	commonAjaxFunction("super_resolution?input=" + params, uiCallBackFunc);
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
		
		},

	});
}
