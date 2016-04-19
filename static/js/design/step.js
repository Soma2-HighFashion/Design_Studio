function StepOne(nextStep) {
	this.next = nextStep;
}

StepOne.prototype.progress = function() {
	// ....
	console.log("Step 1. Process");		
	progress_ui(this.next);
}

function StepTwo(nextStep) {
	this.next = nextStep;
}

StepTwo.prototype.progress = function() {
	// ....
	progress_ui(this.next);
}

function StepThree(nextStep) {
	this.next = nextStep;
}

StepThree.prototype.progress = function() {
	// ....
	progress_ui(this.next);
}

function StepFour(nextStep) {
	this.next = nextStep;
}

StepFour.prototype.progress = function() {
	// ....
	progress_ui(this.next);
}


