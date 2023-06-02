// This function sets a message in the specified form element based on the provided type and message
export function setFormMessage(formElement, type, message) {
  const messageElement = formElement.querySelector(".form__message");

  messageElement.textContent = message;
  messageElement.classList.remove(
    "form__message--success",
    "form__message--error",
    "text-hidden"
  );
  messageElement.classList.add(`form__message--${type}`);

  setTimeout(() => {
    messageElement.classList.add("text-hidden");
  }, 3000);
}

// Shows the register form and hides the login form. 
export function showRegister() {
  const loginForm = document.querySelector("#login");
  const createAccountForm = document.querySelector("#createAccount");

  loginForm.classList.add("form--hidden");
  createAccountForm.classList.remove("form--hidden");
}

// Shows the login form and hides the register form. 
export function showLogin() {
  const loginForm = document.querySelector("#login");
  const createAccountForm = document.querySelector("#createAccount");

  loginForm.classList.remove("form--hidden");
  createAccountForm.classList.add("form--hidden");
}
