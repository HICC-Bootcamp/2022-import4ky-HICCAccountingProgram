let left_checkboxes = document.querySelectorAll("input[name = 'left_checkbox[]']");
let right_checkboxes = document.querySelectorAll("input[name = 'right_checkbox[]']");

function checkAll(myCheckBox) {
	let myCheckBoxId = myCheckBox.getAttribute('id');

	if(myCheckBox.checked === true && myCheckBoxId === 'left_all_check') {
		left_checkboxes.forEach(function(checkbox)
		{
			checkbox.checked = true;
		});
	}

	else if(myCheckBox.checked === true && myCheckBoxId === 'right_all_check') {
		right_checkboxes.forEach(function(checkbox)
		{
			checkbox.checked = true;
		});
	}
	else if(myCheckBox.checked === false && myCheckBoxId === 'left_all_check') {
		left_checkboxes.forEach(function(checkbox)
		{
			checkbox.checked = false;
		});
	}

	else if(myCheckBox.checked === false && myCheckBoxId === 'right_all_check') {
		right_checkboxes.forEach(function(checkbox)
		{
			checkbox.checked = false;
		});
	}
}