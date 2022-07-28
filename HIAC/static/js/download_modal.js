const modal = document.getElementById('download_modal_feed');
const buttonAddFeed = document.getElementById('download_excel');

buttonAddFeed.addEventListener("click", e => {
    modal.style.top = window.pageYOffset + 'px';

    modal.style.display = "flex";
    document.body.style.overflowY = "hidden";

});

const buttonCloseModal = document.getElementById('close_download_modal');

buttonCloseModal.addEventListener("click", e => {
   modal.style.display = "none";
   document.body.style.overflowY = "visible";
});