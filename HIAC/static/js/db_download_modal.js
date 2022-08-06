const db_down_modal = document.getElementById('db_download_modal_feed');
const db_down_buttonAddFeed = document.getElementById('db_download_excel');

db_down_buttonAddFeed.addEventListener("click", e => {
    db_down_modal.style.top = window.pageYOffset + 'px';

    db_down_modal.style.display = "flex";
    document.body.style.overflowY = "hidden";

});

const db_download_buttonCloseModal = document.getElementById('db_close_download_modal');

db_download_buttonCloseModal.addEventListener("click", e => {
   db_down_modal.style.display = "none";
   document.body.style.overflowY = "visible";
});