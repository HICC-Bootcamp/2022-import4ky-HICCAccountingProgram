const modal = document.getElementById('find_modal_feed');
const buttonAddFeed = document.getElementById('find');

buttonAddFeed.addEventListener("click", e => {
    modal.style.top = window.pageYOffset + 'px';

    modal.style.display = "flex";
    document.body.style.overflowY = "hidden";

});

const buttonCloseModal = document.getElementById('close_modal');

buttonCloseModal.addEventListener("click", e => {
   modal.style.display = "none";
   document.body.style.overflowY = "visible";
});

const dateCheckbox = document.getElementById('date_feed');

const detailCheckbox = document.getElementById('detail_feed');
const balanceCheckbox = document.getElementById('balance_feed');
const memoCheckbox = document.getElementById('memo_feed');

function dateInputManage() {

     const startDate = document.getElementById('start_day');
     const endDate = document.getElementById('end_day');

     if (dateCheckbox.checked === true) {
        startDate.disabled = false;
        endDate.disabled = false;
    }
    else {
        startDate.disabled = true;
        endDate.disabled = true;
    }
}

function detailInputManage() {

     const detailInput = document.getElementById('detail_input');

     if (detailCheckbox.checked === true) {
        detailInput.disabled = false;
    }
    else {
        detailInput.disabled = true;
    }
}


function balanceInputManage() {

     const balanceInput = document.getElementById('balance_input');

     if (balanceCheckbox.checked === true) {
        balanceInput.disabled = false;
    }
    else {
        balanceInput.disabled = true;
    }
}


function memoInputManage() {

     const memoInput = document.getElementById('memo_input');

     if (memoCheckbox.checked === true) {
        memoInput.disabled = false;
    }
    else {
        memoInput.disabled = true;
    }
}

let checkboxes = [dateCheckbox, detailCheckbox, balanceCheckbox, memoCheckbox];

