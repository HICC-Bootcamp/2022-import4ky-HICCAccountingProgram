const question_modal = document.getElementById('question_modal_feed');
const question_buttonAddFeed = document.getElementById('question');

question_buttonAddFeed.addEventListener("click", e => {
    question_modal.style.top = window.pageYOffset + 'px';

    question_modal.style.display = "flex";
    document.body.style.overflowY = "hidden";

});

const question_buttonCloseModal = document.getElementById('close_question_modal');

question_buttonCloseModal.addEventListener("click", e => {
   question_modal.style.display = "none";
   document.body.style.overflowY = "visible";
});