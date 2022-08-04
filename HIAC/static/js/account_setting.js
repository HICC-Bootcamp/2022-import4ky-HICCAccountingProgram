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

function alert_result_database_button() {

	if (database_alert_result === "True") {
		alert("정상적으로 데이터베이스에 반영되었습니다.");
	}
	else {
		alert("error");
	}
}