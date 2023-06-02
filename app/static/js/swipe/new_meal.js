const btn = document.querySelector("button");
const post = document.querySelector(".post");
const review = document.querySelector(".review");
const edit = document.querySelector(".edit");
const container = document.querySelector(".container")
btn.onclick = () => {
    review.style.display = "none";
    post.style.display = "block";
    // Add a click event listener to the edit element
    edit.onclick = () => {
        review.style.display = "block";
        post.style.display = "none";
    }
    return false;
}
