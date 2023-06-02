const modalContainers = document.getElementsByClassName("modal-container");
const modals = document.getElementsByClassName("modal");

const hideModal = (modelContainer) => {
  if (modelContainer.classList.contains("visible")) {
    modelContainer.classList.remove("visible");
  }
};

// Prevent the modal container from disappearing if we click on it
for (const modal of modals) {
  modal.addEventListener("click", (event) => {
    event.stopPropagation();
  });
}

// Hides the modal container if we click outside the actual modal
for (const modelContainer of modalContainers) {
  modelContainer.addEventListener("click", () => {
    hideModal(modelContainer);
  });
}
