document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll('.star-click');
    if(stars) {
        stars.forEach(function(element, index) {
            element.addEventListener('click', function() {
                for (let i = index; i < stars.length; i++) {
                    stars[i].classList.add('star-yellow');
                }
                for (let i = 0; i < index; i++) {
                    stars[i].classList.remove('star-yellow');
                }
            });
        });
    }


    const formReview = document.getElementById('formReview');
    const reviewValueInput = document.getElementById('review_value');
    reviewValueInput.removeAttribute('required');
    if (formReview) {
        formReview.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const starYellowCount = document.querySelectorAll('.star-yellow').length;
        
        reviewValueInput.value = starYellowCount;
        formReview.submit();
      });
    }   
});
