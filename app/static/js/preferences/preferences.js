import { getImageFromGoogleImages } from "../integrations/google.js";
import { get, post } from "../_api.js";
import { initPlacesAPI } from "../_helper.js";

const locationInput = document.querySelector("#location_input_preferences");
// Initialize the Google Places API for the location input element
initPlacesAPI("location_input_preferences", (newValue) => {
  currentPreferences.location = newValue.formatted_address;
  saveOtherPreferences();
});

// Add an event listener to the range input element to update the range preference
const rangeInput = document.querySelector("#range_input_preferences");
rangeInput.addEventListener("change", (event) => {
  currentPreferences.range = event.target.value;
  saveOtherPreferences();
});

// Initialize variables for the selected cuisine types and current preferences
let typesSelected = [];
let currentPreferences = {};

// Send a POST request to save the user's location and range preferences to the server
const saveOtherPreferences = async () => {
  await post(
    "/preferences/update_preferences",
    { range: currentPreferences.range, location: currentPreferences.location },
    undefined,
    undefined,
    false
  );
};

// Send a GET request to retrieve the user's current preferences from the server
const getCurrentPreferences = async (pills) => {
  const { data, status } = await get("/preferences/get_preferences");
  currentPreferences = data.preferences;
  typesSelected = currentPreferences.cuisine.map(
    (preference) => preference.name
  );


  // Add the "selected" class to the cuisine type that have already been selected by the user
  for (const pill of pills) {
    const pillText = pill.querySelector("span").innerHTML;
    if (typesSelected.includes(pillText)) {
      pill.classList.add("selected");
    }
  }

  locationInput.value = currentPreferences.location;
  rangeInput.value = currentPreferences.range;
};

// Add images to the cuisine types and set up event listeners to update the user's preferences
const addImagesToPills = async () => {
  const pills = document.getElementsByClassName("cousine-pill");
  getCurrentPreferences(pills);

  for (const pill of pills) {
    const pillImg = pill.querySelector("img");
    const pillText = pill.querySelector("span").innerHTML;
    const googleImg = await getImageFromGoogleImages(
      `${pillText} cuisine cute png icon filetype:png`,
      undefined,
      false
    );
    pillImg.src = googleImg;

    // Add an event listener to the cuisine type to update the user's preferences
    pill.addEventListener("click", async () => {
      if (typesSelected.includes(pillText)) {
        typesSelected = typesSelected.filter((type) => type !== pillText);
        pill.classList.remove("selected");
        currentPreferences.cuisine = currentPreferences.cuisine.filter(
          (cuisine) => cuisine.name !== pillText
        );

        await post(
          "/preferences/remove_preferences_type",
          { uuid: pill.getAttribute("id") },
          undefined,
          undefined,
          false
        );
        // If the pill is not already selected, add it to the list of selected types and preferences
      } else {
        typesSelected.push(pillText);
        pill.classList.add("selected");
        currentPreferences.cuisine.push({ uuid: pill.getAttribute("id") });

        // Send a request to the server to add the cuisine type to the user's preferences
        await post(
          "/preferences/add_preferences_type",
          currentPreferences,
          undefined,
          undefined,
          false
        );
      }
    });
  }
};

document.addEventListener("DOMContentLoaded", () => addImagesToPills());
