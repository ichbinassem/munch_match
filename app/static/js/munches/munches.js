import { remove } from "../_api.js";
import { getImageFromGoogleImages } from "../integrations/google.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

const munchImages = document.getElementsByClassName("munch-image");
const munches = document.getElementsByClassName("matched_dish");

// Load the images for matches using Google Images API
const loadMatchesImages = async () => {
  for (const image of munchImages) {
    if (image.getAttribute("src") === "None") {
      const newSrc = await getImageFromGoogleImages(
        image.getAttribute("alt"),
        undefined,
        false
      );
      image.src = newSrc;
    }
  }
};

//Load the munches and attach event listeners to their delete buttons
const loadMunches = async () => {
  for (const munch of munches) {
    // Loop through all the elements within class "matched_dish"
    const deleteButton = munch.querySelector(".delete-btn");
    deleteButton.addEventListener("click", async () => {
      try {
        const status = await remove(
          "/munches",
          munch.getAttribute("id"),
          undefined,
          undefined,
          false
        );
        // If the status is 204 (No Content), remove the current munch element and display a success message
        if (status === 204) {
          munch.remove();
          successToast("Munch deleted successfully");
          return;
        }

        errorToast("Something went wrong. Please try again");
      } catch (error) {
        errorToast("Something went wrong. Please try again");
      }
    });
  }
};

loadMatchesImages();
loadMunches();
