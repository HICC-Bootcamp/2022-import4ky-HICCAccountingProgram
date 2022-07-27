let checkboxes = document.querySelectorAll("input[name = 'left_checkbox[]']");

function checkAll(myCheckBox) {
	if(myCheckBox.checked === true) {
		checkboxes.forEach(function(checkbox)
		{
			checkbox.checked = true;
		});
	}
	else {
		checkboxes.forEach(function(checkbox)
		{
			checkbox.checked = false;
		});
	}
}