// Object holding the HTML content for each page
const pages = {
  // Login Page
  login: `
    <h2>Login</h2>
    <form>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" placeholder="Enter email">
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" placeholder="Enter password">
      </div>
      <button type="button" class="btn btn-primary" onclick="login()">Login</button>
    </form>
  `,

  // Home Page
  home: `
    <div class="home-page">
      <div>
        <h2>Welcome to MedReminder</h2>
        <p>Never miss a dose again! Set reminders for your medications and stay healthy.</p>
        <button class="btn btn-success" onclick="loadPage('medication')">Set a Reminder</button>
      </div>
    </div>
  `,

  // Medication Page
  medication: `
    <div class="medication-page">
      <div>
        <h2>Set Medication Reminder</h2>
        <form>
          <div class="mb-3">
            <label for="medName" class="form-label">Medicine Name</label>
            <input type="text" class="form-control" id="medName" placeholder="Enter medicine name">
          </div>
          <div class="mb-3">
            <label for="medTime" class="form-label">Time</label>
            <input type="time" class="form-control" id="medTime">
          </div>
          <button type="button" class="btn btn-success" onclick="setReminder()">Set Reminder</button>
        </form>
        <h4 class="mt-3">Upcoming Reminders:</h4>
        <ul id="reminderList"></ul>
      </div>
    </div>
  `,

  // About Page
  about: `
    <div class="about-page">
      <div>
        <h2>About MedReminder</h2>
        <p>MedReminder helps individuals and caregivers track their medications efficiently.</p>
        <p>Features include:</p>
        <ul style="text-align:left; display:inline-block;">
          <li>Set multiple medication reminders</li>
          <li>Receive notifications when it's time to take your medicine</li>
          <li>Easy-to-use and responsive design</li>
        </ul>
      </div>
    </div>
  `,

  // Logout Page
  logout: `
    <div class="logout-page">
      <div>
        <h2>You have been logged out</h2>
        <p>Thank you for using MedReminder.</p>
        <button class="btn btn-primary" onclick="loadPage('login')">Login Again</button>
      </div>
    </div>
  `
};

// Function to show or hide the navbar based on the page
function updateNavbar(page) {
  const navbar = document.getElementById("navbar");
  if (page === "login" || page === "logout") {
    navbar.style.display = "none";
  } else {
    navbar.style.display = "block";
  }
}

// Function to load a page dynamically
function loadPage(page) {
  updateNavbar(page);
  document.getElementById("content").innerHTML = pages[page] || "<h2>Page Not Found</h2>";
}

// Default page (Login) when DOM loads
document.addEventListener("DOMContentLoaded", function () {
  loadPage("login");
});

// Login function
function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (email === "admin@example.com" && password === "12345") {
    alert("Login Successful!");
    loadPage("home");
  } else {
    alert("Invalid email or password!");
  }
}

// Array to store medication reminders
let reminders = [];

// Function to set a medication reminder
function setReminder() {
  const medName = document.getElementById("medName").value;
  const medTime = document.getElementById("medTime").value;

  if (!medName || !medTime) {
    alert("Please enter both medicine name and time!");
    return;
  }

  // Create a Date object for the reminder time
  const now = new Date();
  let reminderTime = new Date(now.toDateString() + " " + medTime);

  // If the reminder time has already passed today, schedule it for tomorrow
  if (reminderTime <= now) {
    reminderTime.setDate(reminderTime.getDate() + 1);
  }

  // Store the reminder details
  reminders.push({ name: medName, time: reminderTime });

  // Update the upcoming reminders list
  const reminderList = document.getElementById("reminderList");
  const listItem = document.createElement("li");
  listItem.innerText = `${medName} at ${medTime}`;
  reminderList.appendChild(listItem);

  // Calculate the delay (in milliseconds) until the reminder time
  const delay = reminderTime - now;
  setTimeout(() => {
    alert(`It's time for your medication: ${medName}`);
  }, delay);
}
