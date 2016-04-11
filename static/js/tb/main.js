$( document ).ready(function() {
	console.log( "ready!" );

	// Dashboard
	selectImageData("", makeCountList, $("#tb_image_total_count"));
	selectImageData("modality=1", makeCountList, $("#tb_modality_cr_count"));
	selectImageData("modality=2", makeCountList, $("#tb_modality_dx_count"));
	
	categoryCount = 3;
	for (i=1; i<=categoryCount; i++) {
		selectImageData("modality=1", makeCountList, $("#tb_knta_category"+i+"_cr_count"));
		selectImageData("modality=2", makeCountList, $("#tb_knta_category"+i+"_dx_count"));
		selectImageData("", makeCountList, $("#tb_knta_category"+i+"_image_count"));
		selectImageSize("category="+i, makeImageSizeList, $("#tb_knta_category"+i+"_image_size"));
		selectROCSummary(
			"category="+i, makeRcTemplate, 
			[ $("#tb_knta_category"+i+"_roc_table"), $("#tb_knta_category"+i+"_roc_chart") ]
		);
		selectRDCSummary(
			"category="+i, makeRcTemplate, 
			[ $("#tb_knta_category"+i+"_rdc_table"), $("#tb_knta_category"+i+"_rdc_chart") ]
		);
	}

});

