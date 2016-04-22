function StepOne(nextStep) {
	this.next = nextStep;
}

StepOne.prototype.progress = function() {
	// ....
	console.log("Step 1. Process");		
}

function StepTwo(nextStep) {
	this.next = nextStep;
}

StepTwo.prototype.progress = function() {
	// ....
}

function StepThree(nextStep) {
	this.next = nextStep;
}

StepThree.prototype.progress = function() {
	// ....
}

function StepFour(nextStep) {
	this.next = nextStep;
}

StepFour.prototype.progress = function() {
	// ....
}


