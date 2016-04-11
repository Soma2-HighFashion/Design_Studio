
// ========================== Server API ============================//

var ctxPath = ""; // 현재 주소로 수정
var jsonFormat = '?format=json&';

function select(api, query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/' + api + "/"+ jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectImageData(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/images/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectImageSize(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/images/totalsize/?' + query, UICallBackFunc, UICallBackParam);
}

function selectImageCompress(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/images/compress/?' + query, UICallBackFunc, UICallBackParam);
}

function selectImageYears(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/images/years/?' + query, UICallBackFunc, UICallBackParam);
}

function selectROCSummary(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/images/roc_summary/?' + query, UICallBackFunc, UICallBackParam);
}

function selectRDCSummary(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/images/rdc_summary/?' + query, UICallBackFunc, UICallBackParam);
}

function selectCategory(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/category/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectDataType(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/data_type/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectTask(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/task/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectDataSource(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/data_source/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectModality(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/modality/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectRefinedClass(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/refined_class/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectOriginalClass(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/original_class/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

function selectDiagnosedClass(query, UICallBackFunc, UICallBackParam) {
	commonAjaxFunction('/api/diagnosed_class/' + jsonFormat + query, UICallBackFunc, UICallBackParam);
}

/* ----- Ajax  -----*/

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
