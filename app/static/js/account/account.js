import { patch } from "../_api.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

// Get the elements that we need to manipulate
const nameEditButton = document.querySelector("#edit-name-button");
const emailEditButton = document.querySelector("#edit-email-button");
const nameEditInput = document.querySelector("#edit-name-input");
const emailEditInput = document.querySelector("#edit-email-input");
const nameValue = document.querySelector("#name-value");
const emailValue = document.querySelector("#email-value");
const mainNameValue = document.querySelector("#main-name-value");
const mainEmailValue = document.querySelector("#main-email-value");


// Function to save account settings
const saveSettings = async (body) => {
  if (body.email && body.name) {
    try {
      // Send a PATCH request to update the account details
      const status = await patch("/account", body);

      // If the request is successful, show a success message and return true
      if (status === 204) {
        successToast("Account updated successfully!");
        return true;
      }

      // If the request fails, show an error message and return false
      errorToast("Something went wrong. Please try again");
      return false;
    } catch (error) {
      errorToast(error.message);
      return false;
    }
  } else {
    // If email and name are not present in the input object, show an error message 
    errorToast("Please fill the email and password");
    return false;
  }
};

// Event listener for editing the name
nameEditButton.addEventListener("click", () => {
  if (nameEditButton.innerHTML === "Edit") {
    nameEditInput.classList.remove("hidden");
    nameValue.classList.add("hidden");
    nameEditButton.innerHTML = "Save";
  } else {
    if (
      saveSettings({ email: emailEditInput.value, name: nameEditInput.value })
    ) {
      nameValue.innerHTML = mainNameValue.innerHTML = nameEditInput.value;
      nameEditInput.classList.add("hidden");
      nameValue.classList.remove("hidden");
      nameEditButton.innerHTML = "Edit";
    }
  }
});

// Event listener for editing the email
emailEditButton.addEventListener("click", () => {
  if (emailEditButton.innerHTML === "Edit") {
    emailEditInput.classList.remove("hidden");
    emailValue.classList.add("hidden");
    emailEditButton.innerHTML = "Save";
  } else {
    if (
      saveSettings({ email: emailEditInput.value, name: nameEditInput.value })
    ) {
      // If the saveSettings function returns true, update the email values in the display and hide the edit input
      emailValue.innerHTML = mainEmailValue.innerHTML = emailEditInput.value;
      emailEditInput.classList.add("hidden");
      emailValue.classList.remove("hidden");
      emailEditButton.innerHTML = "Edit";
    }
  }
});
