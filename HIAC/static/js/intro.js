
function passwordInputActive() {
    document.getElementById("pwBtn").disabled = false;
    document.getElementById("pass").disabled = false;
}

function passwordInputInactive() {
    document.getElementById("pwBtn").disabled = true;
    document.getElementById("pass").disabled = true;
}

function pageMoveActive() {
    document.getElementById("pageMove").disabled = false;
}

if (url) {
    passwordInputActive();
}

if (left_table) {
     passwordInputInactive();
     pageMoveActive();
}