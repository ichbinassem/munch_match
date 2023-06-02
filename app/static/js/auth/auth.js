import { showLogin, showRegister } from "./authHelper.js";


// Add a click event listener to the "Create Account" link
document.querySelector("#linkCreateAccount").addEventListener("click", (e) => {
  e.preventDefault();
  showRegister();
});

// Add a click event listener to the "Login" link
document.querySelector("#linkLogin").addEventListener("click", (e) => {
  e.preventDefault();
  showLogin();
});
