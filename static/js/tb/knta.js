$( document ).ready(function() {
	console.log( "ready!" );
	
	// DashBoard
	selectImageData("", makeCountList, $("#Image_total_count"));
	selectCategory("", makeDashboardList, $("#Image_category_overview"));
	selectDataType("", makeDashboardList, $("#Image_datatype_overview"));
	selectModality("", makeDashboardList, $("#Image_modality_overview"));
	selectRefinedClass("", makeDashboardList, $("#Image_refined_oc_overview"));
	selectRefinedClass("", makeDashboardList, $("#Image_refined_dc_overview"));
	
	// SearchTag
	selectCategory("", makeSearchTagList, $("#Image_category_tags"));
	selectDataType("", makeSearchTagList, $("#Image_datatype_tags"));
	selectModality("", makeSearchTagList, $("#Image_modality_tags"));
	selectRefinedClass("", makeSearchTagList, $("#Image_refined_oc_tags"));
	selectRefinedClass("", makeSearchTagList, $("#Image_refined_dc_tags"));
	selectImageYears("", makeYearsList, $("#Image_year_tags"));
	
	clickButton("sex");

	// Image Data Search Table
	var query = "";
	var searchInput = $("#Image_search_input");
	var searchBtn = $("#Image_search_btn");
	var downloadAllBtn = $("#Image_download_all_btn");	

	downloadAllBtn.click(function() {
		initProgress();

		var totalSize = $("#Image_total_size").attr("image_size");
		makeImageProgressBar(totalSize/1000);
		
		var progress = $("#Image_progress");
		progress.show();

		var history = $("#Image_download_history");
		setTimeout(function() {
			history.append("<p> Start Compress image files.. </p>");
		}, 1000);

		if (searchInput.val() == "")
			query = getQuerys();
		selectImageCompress(query, makeImageCmdList);

		// *** Direct Download *** //
		//var iframe = $("#Image_download_iframe");
		//var download_url = ctxPath + '/api/images/download?' + query;
		//iframe.attr("src", download_url);
	});
    
	searchInput.keypress(function(e) {
      // 13 : Enter
	  if (e.which == 13) {
		e.preventDefault();

		query = searchInput.val();
		searchQuery(query);
      }
    });

	function initProgress() {
		$("#Image_progress_bar").css('width', '0%');
		
		var history = $("#Image_download_history");
		var cmd = $("#Image_download_cmd");
		history.text(""); cmd.text("");

		var loader = $("#Image_download_loader");
		loader.hide();
	}

});

