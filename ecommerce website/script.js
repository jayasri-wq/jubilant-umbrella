let cart = [];

function showPage(page) {
    // Hide all pages
    document.querySelectorAll(".page").forEach(div => div.classList.add("hide"));
    // Show the selected page
    document.getElementById(page).classList.remove("hide");

    if (page !== "login") {
        localStorage.setItem("currentPage", page);
    }
}

function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (email === "user@example.com" && password === "password123") {
        alert("Login Successful!");
        showPage('home');
    } else {
        alert("Invalid email or password!");
    }
    return false; // Prevent form submission
}

function addToCart(product, price) {
    cart.push({ product, price });
    alert(`${product} has been added to your cart.`);

    // Update the cart display on cart page
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cart-items');
    const totalPriceElement = document.getElementById('total-price');
    cartItemsContainer.innerHTML = ''; // Clear current cart items

    let totalPrice = 0;
    cart.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('cart-item');
        itemElement.innerHTML = `${item.product} - $${item.price}`;
        cartItemsContainer.appendChild(itemElement);
        totalPrice += item.price;
    });

    totalPriceElement.textContent = totalPrice;
}

function placeOrder() {
    if (cart.length === 0) {
        alert("Your cart is empty. Please add items to cart.");
        return;
    }

    alert("Your order has been placed successfully!");
    cart = []; // Empty the cart
    updateCartDisplay();
}

function logout() {
    alert("Logged out successfully!");
    showPage('login');
    localStorage.removeItem("currentPage");
}

// Load last visited page (if logged in)
document.addEventListener("DOMContentLoaded", () => {
    let lastPage = localStorage.getItem("currentPage");
    if (lastPage) showPage(lastPage);
});
