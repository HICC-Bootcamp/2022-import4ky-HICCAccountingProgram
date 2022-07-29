const down_modal = document.getElementById('download_modal_feed');
const down_buttonAddFeed = document.getElementById('download_excel');

down_buttonAddFeed.addEventListener("click", e => {
    down_modal.style.top = window.pageYOffset + 'px';

    down_modal.style.display = "flex";
    document.body.style.overflowY = "hidden";

});

const download_buttonCloseModal = document.getElementById('close_download_modal');

download_buttonCloseModal.addEventListener("click", e => {
   down_modal.style.display = "none";
   document.body.style.overflowY = "visible";
});