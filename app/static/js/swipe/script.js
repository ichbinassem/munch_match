import { post, get } from "../_api.js";
import { getFormData, initPlacesAPI } from "../_helper.js";
import { getImageFromGoogleImages } from "../integrations/google.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

// Get DOM elements
const swipper = document.getElementById("swipper");
const swipe_forward = document.getElementById("swipe_forward");
const swipe_backward = document.getElementById("swipe_backward");
const newDishButton = document.getElementById("new_dish");
const newDishModalContainer = document.getElementById("add_new_dish_modal");
const newDishModal = newDishModalContainer.getElementsByClassName("modal")[0];
const newDishForm = document.getElementById("new_dish_form");

// Initialize Places API and update location
initPlacesAPI("location_input_new_meal", (newValue) => {
  currentPreferences.location = newValue.formatted_address;
  saveOtherPreferences();
});

let meals = [];
let tempMeals = [];

// Get initial dishes from the server
const getInitialDishes = async () => {
  const response = await get(`/swipe/meals`);
  meals = response.data.data;
  const tempMeals = [];
  for (const dish of response.data.data) {
    tempMeals.push(await createDish(dish, false));
  }

  for (const meal of tempMeals) {
    swipper.append(meal);
  }
};

// Create a new dish with the given parameters (picture, name, price, rate, location)
async function createDish(newDish, append = true) {
  const picture = await getImageFromGoogleImages(
    newDish.name,
    undefined,
    false
  );
  const dish = new Dish({
    picture: newDish.picture || picture,
    price: newDish.price,
    name: newDish.name,
    location: newDish.location || "",
    rate: newDish.rate,

    // Handle events when a dish is liked or disliked (swiped to the right or to the left)
    onDishLiked: () => {
      swipe_forward.style.animationPlayState = "running";
      swipe_forward.classList.toggle("trigger");
      getNextMeal(newDish.uuid, "right");
    },
    onDishDisliked: () => {
      swipe_backward.style.animationPlayState = "running";
      swipe_backward.classList.toggle("trigger");
      getNextMeal(newDish.uuid, "left");
    },
  });

  if (append) {
    swipper.prepend(dish.element);
  } else {
    return dish.element;
  }
}

function updateDishes() {
  const dishes = swipper.querySelectorAll(".dish:not(.dismissing)");
  dishes.forEach((dish, index) => {
    dish.style.setProperty("--i", index);
  });
}

// Get the next meal to be displayed
const getNextMeal = async (swippedMealUUID, direction) => {
  const response = await post(
    `/swipe/swipe/${swippedMealUUID}/${direction}`,
    {},
    undefined,
    undefined,
    false
  );
  const status = response.status;
  const newMeals = response.data.data;
  const exitingMeals = [...meals].map((card) => card.uuid);
  const newMeal = newMeals.filter(
    (meal) => !exitingMeals.includes(meal.uuid) && meal.uuid !== swippedMealUUID
  )[0];

  if (newMeal) {
    meals.push(newMeal);
    createDish(newMeal);
  }
};

getInitialDishes();
updateDishes();

// Event listener for the newDishButton that displays the add new dish modal when clicked
newDishButton.addEventListener("click", () => {
  newDishModalContainer.classList.add("visible");
});

// Event listener for the newDishModalContainer that hides the modal when clicked outside of the modal
newDishModalContainer.addEventListener("click", () => {
  newDishModalContainer.classList.remove("visible");
});

newDishModal.addEventListener("click", (event) => {
  event.stopPropagation();
});

// Event listener for the newDishForm that sends a POST request to add a new dish when submitted
newDishForm.addEventListener("submit", async (event) => {
  try {
    event.preventDefault();
    const obj = getFormData(event, newDishForm);
    const newSrc = await getImageFromGoogleImages(obj["name"]);
    obj.picture = newSrc;
    const { data, status } = await post("/meal", obj);

    // If the status code is 201 (Created), hide the modal and display a success message, then create a new dish and update the list of dishes
    if (status === 201) {
      newDishModalContainer.classList.remove("visible");
      successToast("Meal added successfully!");
      createDish(data.newMeal);
      updateDishes();

      return;
    }
// If the status code is not 201, display an error message
    errorToast("An error has occurred. Try again");
  } catch (error) {
    errorToast(error.message);
  }
});
