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

function searchNeighbors(params, uiCallBackFunc) {
	commonAjaxFunction("search_neighbors?num=12&input=" + params, uiCallBackFunc);
}

function imageHandler(uid, method, params, callBack) {
	if (uid != "") {
		uid += "/";
	}
	ajaxCRUDFunction("api/image/" + uid , method, params, callBack);
}

function designHandler(uid, method, params, callBack) {
	if (uid != "") {
		uid += "/";
	}
	ajaxCRUDFunction("api/design/" + uid, method, params, callBack);
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
		error : function(request, status, error) {
			//console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
			alert("오류가 발생하였습니다. 다시 시도해주세요.");	
		},

	});
}

function ajaxCRUDFunction(urlStr, method, params, callBack) {

	var callUrl = ctxPath + urlStr;

	$.ajax({
		type : method,
		url : callUrl,
		data : params,
		success : function(response) {
			callBack(response);
		},
		error : function(request, status, error) {
			console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
			alert("오류가 발생하였습니다. 다시 시도해주세요..");	
		},

	});

}

var image = {
	"uid": "",
	"gender": "",
	"category": "",
	"text": "",
}

var design = {
	"id": 0,
	"uid": "",
	"history_uid": "",
	"history_text": "",
	"filtered": false,
	"like": 0
}
