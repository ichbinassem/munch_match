// Imports
import { post } from "../_api.js";
import { getFormData, removeLoading } from "../_helper.js";
import { setFormMessage, showLogin } from "./authHelper.js";

// Get register form from the DOM
const registerForm = document.getElementById("createAccount");

registerForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    // Get data of the register form
    const obj = getFormData(event, registerForm);

    if (obj.password !== obj.repeatPassword) {
      setFormMessage(registerForm, "error", "Your passwords do not match");
      return;
    }

    delete obj.repeatPassword;
    // Try to register with the data from the form
    const { data, status } = await post("/auth/register", obj);

    if (status === 201) {
      showLogin();
      return;
    }

    setFormMessage(registerForm, "error", data.message);
    removeLoading();
  } catch (error) {
    setFormMessage(registerForm, "error", error.message);
    removeLoading();
  }
});
