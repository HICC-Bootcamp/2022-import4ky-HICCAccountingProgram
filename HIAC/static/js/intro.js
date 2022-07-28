
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

function PasswordError() {
    alert("패스워드가 일치하지 않습니다.");
}

if(password_error === "True") {
    PasswordError();
    passwordInputActive();
}
else {
    if (url) {
        passwordInputActive();
    }

    if (left_table) {
     passwordInputInactive();
     pageMoveActive();
    }
}
