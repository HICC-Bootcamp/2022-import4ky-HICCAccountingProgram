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
        $("#search_date_feed").val(0);

    }
    else {
        startDate.disabled = true;
        endDate.disabled = true;
        $("#search_date_feed").val(1);
    }
}

function showDetailInputManage() {

     const detailInput = document.getElementById('search_detail_input');

     if (showDetailCheckbox.checked === true) {
        detailInput.disabled = false;
        $("#search_detail_feed").val(0);
    }
    else {
        detailInput.disabled = true;
        $("#search_detail_feed").val(1);
    }
}


function showBalanceInputManage() {

     const balanceInput = document.getElementById('search_balance_input');

     if (showBalanceCheckbox.checked === true) {
        balanceInput.disabled = false;
        $("#search_balance_feed").val(0);
    }
    else {
        balanceInput.disabled = true;
        $("#search_balance_feed").val(1);
    }
}


function showMemoInputManage() {

     const memoInput = document.getElementById('search_memo_input');

     if (showMemoCheckbox.checked === true) {
        memoInput.disabled = false;
        $("#search_memo_feed").val(0);
    }
    else {
        memoInput.disabled = true;
        $("#search_memo_feed").val(1);
    }
}
