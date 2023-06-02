import { post } from "../_api.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

const addReviewButtons = document.getElementsByClassName("review-btn");
const reviewModalContainer =
  document.getElementsByClassName("modal-container")[0];
const hearts = document.getElementsByTagName("input");
const reviewSubmitButton = document.getElementById("review-submit");
const reviewModal = reviewModalContainer.getElementsByClassName("review")[0];

let currentDishId = 0;

// Looping through each 'addReviewButton' element and adding a click event listener to it
for (const addReviewButton of addReviewButtons) {
  addReviewButton.addEventListener("click", () => {
    reviewModalContainer.classList.add("visible");
    // Extracting the ID from the clicked 'addReviewButton' element
    const id = addReviewButton.id.match(/\d+/)[0];
    currentDishId = parseInt(id);
  });
}

// Adding a click event listener to the 'reviewSubmitButton' element
reviewSubmitButton.addEventListener("click", async () => {
  for (const heart of hearts) {
    if (heart.checked) {
      try {
        const rating = heart.id.match(/\d+/)[0];
         // Sending a POST request to the '/review' endpoint with the rating and current dish ID
        const { data, status } = await post(
          "/review",
          { rating, meal_id: currentDishId },
          undefined,
          undefined,
          false
        );

        if (status === 200) {
          // Displaying a success toast message and updating the corresponding meal's rating
          successToast(data.message);
          const correspondingMeal = document.getElementById(
            data.newMeal.meal_id
          );
          const rating =
            correspondingMeal.getElementsByClassName("rating-text")[0];
          rating.innerHTML = "★".repeat(parseInt(data.newMeal.rating));
          reviewModalContainer.classList.remove("visible");
          return;
        }

        errorToast("Something went wrong. Please try again");
      } catch (error) {
        errorToast("Something went wrong. Please try again");
      }
    }
  }
});

reviewModalContainer.addEventListener("click", () => {
  reviewModalContainer.classList.remove("visible");
});

reviewModal.addEventListener("click", (event) => {
  event.stopPropagation();
});
// const btn = document.querySelector("button");
// const post = document.querySelector(".post");
// const review = document.querySelector(".review");
// const edit = document.querySelector(".edit");

// /* the detailed comment widget shows only after the hearts are clicked */
// /* the edit button shows after the review is submitted */

// btn.onclick = () => {
//     review.style.display = "none";
//     post.style.display = "block";
//     edit.onclick = () => {
//         review.style.display = "block";
//         post.style.display = "none";
//     }
//     return false;
// }
