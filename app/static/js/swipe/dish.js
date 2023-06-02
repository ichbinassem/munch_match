class Dish {
  constructor({
    picture,
    price,
    name,
    rate,
    location,
    onDishLiked,
    onDishDisliked,
  }) {
    this.picture = picture;
    this.location = location;
    this.rate = rate;
    this.price = price;
    this.name = name;
    this.onDishLiked = onDishLiked;
    this.onDishDisliked = onDishDisliked;
    // Call private initialization method
    this.#init();
  }

  // Private properties
  #startPoint;
  #offsetX;
  #offsetY;

   // Private method to detect touch capability
  #hasTouchCapability = () => {
    return (
      "ontouchstart" in window ||
      navigator.maxTouchPoints > 0 ||
      navigator.msMaxTouchPoints > 0
    );
  };

  // Private method to initialize the Dish element
  #init = () => {
    const dish = document.createElement("div");
    dish.classList.add("dish");
    dish.style.background = "#F2CF53";

    const imgContainer = document.createElement("div");
    imgContainer.classList.add("img-container");

    const img = document.createElement("img");
    img.src = this.picture;
    img.style.display = "block";
    img.style.margin = "auto";
    img.style.height = "100%";
    imgContainer.append(img);
    dish.append(imgContainer);


    const infoContainer = document.createElement("div");
    infoContainer.classList.add("info-container");
    infoContainer.style.flexDirection = "row";
    infoContainer.style.alignItems = "center";
    infoContainer.style.justifyContent = "space-between";

    const nameAndPrice = document.createElement("div");
    nameAndPrice.style.display = "flex";
    nameAndPrice.style.flexDirection = "row";

    // Function to generate dollar signs based on price
    function generateDollarSigns(price) {
      if (price <= 10) {
        return '<span style="color:#000;">$</span>';
      } else if (price <= 15) {
        return '<span style="color:#000;">$$</span>';
      } else if (price <= 20) {
        return '<span style="color:#000;">$$$</span>';
      } else {
        return '<span style="color:#000;">$$$$</span>';
      }
    }

    // Create the name element and set its properties
    const name = document.createElement("div");
    name.style.fontSize = "24px";
    name.style.color = "black";
    name.innerHTML = `${this.name} ${generateDollarSigns(this.price)}`;
    nameAndPrice.append(name);

    // Create the price element and set its properties
    const price = document.createElement("div");
    price.textContent = "$" + this.price;
    price.style.marginLeft = "auto";
    price.style.color = "#c91818";
    nameAndPrice.append(price);
    infoContainer.append(nameAndPrice);

    // Create the rate and address container and set its properties
    const rateAndAddress = document.createElement("div");
    rateAndAddress.classList.add("rate-container");

    // Create the rate element and set its properties to make it shown using stars
    const rate = document.createElement("div");
    rate.classList.add("rating");
    let stars = "";
    if (this.rate) {
      for (let i = 0; i < this.rate; i++) {
        stars += "★";
      }
    } else {
      stars = "No reviews yet";
    }

    rate.textContent = stars;
    rateAndAddress.append(rate);

    if (this.location) {
      const address = document.createElement("div");
      address.textContent = "📍 " + this.location;
      rateAndAddress.append(address);
      infoContainer.append(rateAndAddress);
    }

    // Create the View on Google Maps button container
    const mapsContainer = document.createElement("div");
    mapsContainer.style.display = "flex";
    mapsContainer.style.flexDirection = "column";
    mapsContainer.style.alignItems = "center";

    // Create the View on Google Maps button and set its text content that will redirect that user to Google Maps
    const viewOnGoogleMapsButton = document.createElement("div");
    viewOnGoogleMapsButton.textContent = "View on Google Maps";
    viewOnGoogleMapsButton.classList.add("maps-button");
    viewOnGoogleMapsButton.addEventListener("click", () => {
      const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
        this.location || this.name
      )}`;
      window.open(mapsUrl, "_blank");
    });
    mapsContainer.append(viewOnGoogleMapsButton);

    this.element = dish;
    // Append the info and maps containers to the dish container
    dish.append(infoContainer);
    dish.append(mapsContainer);

    // Add either touch or mouse events based on the device's capabilities
    if (this.#hasTouchCapability()) {
      this.#TouchEvents();
  } else {
      this.#MouseEvents();
  }
}

  // Event listeners for touch events
  #TouchEvents = () => {
    // Add touchstart event listener to the element
    this.element.addEventListener('touchstart', ({ changedTouches }) => {
      const { clientX, clientY } = changedTouches[0];
      if (!changedTouches[0]) return;
      this.#startPoint = { x: clientX, y: clientY }
      // Add touchmove event listener to the document
      document.addEventListener('touchmove', this.#handleTouchMove);
      // Disable the transition effect
      this.element.style.transition = 'transform 0s';
    });

    // Add touchend and cancel event listeners to the document
    document.addEventListener('touchend', this.#handleTouchEnd);
    document.addEventListener('cancel', this.#handleTouchEnd);
    }


  // Event listeners for mouse events
  #MouseEvents = () => {
    this.element.addEventListener('mousedown', (e) => {
      const { clientX, clientY } = e;
      this.#startPoint = { x: clientX, y: clientY }
      document.addEventListener('mousemove', this.#handleMouseMove);
      this.element.style.transition = 'transform 0s';
    });
    
    document.addEventListener('mouseup', this.#handleMoveUp);

    // Add dragstart event listener to the element to prevent dragging
    this.element.addEventListener('dragstart', (e) => {
      e.preventDefault();
    });
    }


  // Handle movement of the element
  #handleMove = (x, y) => {
    // Calculate the offset between the starting point and the current point
    this.#offsetX = x - this.#startPoint.x;
    this.#offsetY = y - this.#startPoint.y;
    // Calculate the rotation angle based on the offset
    const rotate = this.#offsetX * 0.05;
    this.element.style.transform = `translate(${this.#offsetX}px, ${this.#offsetY}px) rotate(${rotate}deg)`;
    // Check if the element has been swiped past a certain threshold which is 60% of the width of the card
    if (Math.abs(this.#offsetX) > this.element.clientWidth * 0.6) {
      // Call the dismiss method with the appropriate direction (right or left)
      if (this.#offsetX > 0) {
        this.#dismiss(1);
      } else {
        this.#dismiss(-1);
      }
    }
    }

  // Event listener for mousemove event
  #handleMouseMove = (e) => {
    e.preventDefault();
    if (!this.#startPoint) return;
    // Calculate the movement based on the current mouse position
    const { clientX, clientY } = e;
    this.#handleMove(clientX, clientY);
    }

  // Event listener for mouseup event
  #handleMoveUp = () => {
    // Reset the starting point and remove the mousemove event listener
    this.#startPoint = null;
    document.removeEventListener('mousemove', this.#handleMouseMove);
    this.element.style.transform = '';
    }

  // Event listener for touchmove event
  #handleTouchMove = ({ changedTouches }) => {
    if (!this.#startPoint) return;
    const touch = changedTouches[0];
    if (!touch) return;
    // Get the x and y coordinates of the touch point
    const { clientX, clientY } = touch;
    // Call the handleMove function with the touch coordinates
    this.#handleMove(clientX, clientY);
    }


  // Event listener for touchend event
  #handleTouchEnd = () => {
    this.#startPoint = null;
    this.element.removeEventListener('touchmove', this.#handleTouchMove);
    this.element.style.transform = '';
    };

  // Function to dismiss the card in a certain direction
  #dismiss = (direction) => {
    this.#startPoint = null;
    document.removeEventListener('mouseup', this.#handleMoveUp);
    document.removeEventListener('mousemove', this.#handleMouseMove);
    document.removeEventListener('touchend', this.#handleTouchEnd);
    document.removeEventListener('touchmove', this.#handleTouchMove);
    this.element.style.transition = 'transform 1s';
    this.element.style.transform = `translate(${direction * window.innerWidth}px, ${this.#offsetY}px) rotate(${45 * direction}deg)`;
    this.element.classList.add('dismissing');
    // Remove the element from the DOM after 1 second
    setTimeout(() => {
      this.element.remove();
    }, 1000);

    this.onDishDismissed?.();
    // Call the onDishLiked callback function with a boolean value indicating if the card was swiped to the right
    this.onDishLiked?.(direction === 1);
    // Call the onDishDisliked callback function with a boolean value indicating if the card was swiped to the left
    this.onDishDisliked?.(direction === -1);
    }}



