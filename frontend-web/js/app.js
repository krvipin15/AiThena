/* filepath: d:\Academics\AiThena\frontend-web\js\app.js */
const API_BASE = "http://localhost:8000";
let currentUser = null;

// DOM Elements - Declare each element only once
const signInBtn = document.getElementById("signInBtn");
const getStartedBtn = document.getElementById("getStartedBtn");
const loginModal = document.getElementById("loginModal");
const registerModal = document.getElementById("registerModal");
const closeModal = document.getElementById("closeModal");
const closeRegisterModal = document.getElementById("closeRegisterModal");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");

console.log("App.js loaded");
console.log("signInBtn:", signInBtn);
console.log("loginModal:", loginModal);

// Event Listeners - Only add if elements exist
if (signInBtn) signInBtn.addEventListener("click", openLoginModal);
if (getStartedBtn) getStartedBtn.addEventListener("click", openLoginModal);
if (closeModal) closeModal.addEventListener("click", closeLoginModal);
if (closeRegisterModal)
  closeRegisterModal.addEventListener("click", closeRegisterModal);
if (showRegister) showRegister.addEventListener("click", openRegisterModal);
if (showLogin) showLogin.addEventListener("click", openLoginModal);
if (loginForm) loginForm.addEventListener("submit", handleLogin);
if (registerForm) registerForm.addEventListener("submit", handleRegister);

// Modal Functions
function openLoginModal() {
  if (loginModal) loginModal.classList.remove("hidden");
  if (registerModal) registerModal.classList.add("hidden");
}

function openRegisterModal() {
  if (registerModal) registerModal.classList.remove("hidden");
  if (loginModal) loginModal.classList.add("hidden");
}

function closeLoginModal() {
  if (loginModal) loginModal.classList.add("hidden");
}

function closeRegisterModal() {
  if (registerModal) registerModal.classList.add("hidden");
}

// Authentication Functions
async function handleLogin(e) {
  e.preventDefault();
  console.log("Login attempt started");

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  console.log("Email:", email);
  console.log("API_BASE:", API_BASE);

  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const result = await response.json();

    if (result.success) {
      currentUser = { email, password };
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userPassword", password);
      closeLoginModal();
      window.location.href = "dashboard.html";
    } else {
      alert("Login failed: " + result.message);
    }
  } catch (error) {
    alert("Connection error: " + error.message);
  }
}

async function handleRegister(e) {
  e.preventDefault();

  const email = document.getElementById("regEmail").value;
  const password = document.getElementById("regPassword").value;

  try {
    const response = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const result = await response.json();

    if (result.success) {
      alert("Account created successfully! Please sign in.");
      openLoginModal();
    } else {
      alert("Registration failed: " + result.message);
    }
  } catch (error) {
    alert("Connection error: " + error.message);
  }
}

// Close modals when clicking outside
window.addEventListener("click", function (event) {
  if (event.target === loginModal) {
    closeLoginModal();
  }
  if (event.target === registerModal) {
    closeRegisterModal();
  }
});
