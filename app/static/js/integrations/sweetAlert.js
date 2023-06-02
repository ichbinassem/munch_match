//Displays a success modal with a "Success" title and the given text message
export async function successModal(text, callback = () => {}) {
  Swal.fire({
    title: "Success",
    text,
    confirmButtonColor: "#FE760D",
    icon: "success",
    heightAuto: false,
  }).then(callback);
}

// Displays an error modal with an "Error" title and the given text message
export async function errorModal(
  text,
  callback = () => {},
  confirmButtonText = "Ok"
) {
  Swal.fire({
    title: "Error",
    text,
    confirmButtonColor: "#FE760D",
    confirmButtonText,
    icon: "error",
    heightAuto: false,
  }).then(callback);
}

// Displays a warning modal with a "Warning" title and the given text message
export async function warningModal(text, callback = () => {}) {
  Swal.fire({
    title: "Warning",
    text,
    confirmButtonColor: "#FE760D",
    icon: "warning",
    heightAuto: false,
  }).then(callback);
}

// Displays a success toast notification with the given text message.
export async function successToast(text) {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-right",
    iconColor: "white",
    customClass: {
      popup: "colored-toast",
    },
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
  });
  await Toast.fire({
    icon: "success",
    title: text,
  });
}

// Displays an error toast notification with the given text message. 
export async function errorToast(text) {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-right",
    iconColor: "white",
    customClass: {
      popup: "colored-toast",
    },
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
  });
  await Toast.fire({
    icon: "error",
    title: text,
  });
}
