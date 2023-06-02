// Imports
import { post } from "../_api.js";
import { getFormData, removeLoading } from "../_helper.js";
import { setFormMessage } from "./authHelper.js";

// Get login form from the DOM
const loginForm = document.getElementById("login");

loginForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    // Get data of the login form
    const obj = getFormData(event, loginForm);

    // Try to login with the data from the form
    const { status, data } = await post("/auth/login", obj, undefined, false);

    if (status === 200) {
      window.location.href = "/swipe";
      return;
    }

    setFormMessage(loginForm, "error", data.message);
    removeLoading();
  } catch (error) {
    setFormMessage(loginForm, "error", error.message);
    removeLoading();
  }
});
