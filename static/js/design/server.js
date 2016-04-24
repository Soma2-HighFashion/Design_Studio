ctxPath = "" 

function generateImage(api, query, uiCallBackFunc) {
	commonAjaxFunction(api + "?" + query, uiCallBackFunc);
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
