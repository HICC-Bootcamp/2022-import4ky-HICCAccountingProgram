const showDateCheckbox = document.getElementById('search_date_feed');

const showDetailCheckbox = document.getElementById('search_detail_feed');
const showBalanceCheckbox = document.getElementById('search_balance_feed');
const showMemoCheckbox = document.getElementById('search_memo_feed');

function showDateInputManage() {

     const startDate = document.getElementById('search_start_day');
     const endDate = document.getElementById('search_end_day');

     if (showDateCheckbox.checked === true) {
        startDate.disabled = false;
        endDate.disabled = false;
    }
    else {
        startDate.disabled = true;
        endDate.disabled = true;
    }
}

function showDetailInputManage() {

     const detailInput = document.getElementById('search_detail_input');

     if (showDetailCheckbox.checked === true) {
        detailInput.disabled = false;
    }
    else {
        detailInput.disabled = true;
    }
}


function showBalanceInputManage() {

     const balanceInput = document.getElementById('search_balance_input');

     if (showBalanceCheckbox.checked === true) {
        balanceInput.disabled = false;
    }
    else {
        balanceInput.disabled = true;
    }
}


function showMemoInputManage() {

     const memoInput = document.getElementById('search_memo_input');

     if (showMemoCheckbox.checked === true) {
        memoInput.disabled = false;
    }
    else {
        memoInput.disabled = true;
    }
}

