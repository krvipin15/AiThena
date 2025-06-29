const loginForm = document.getElementById("loginForm");
const registerSection = document.getElementById("registerSection");
const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");
const registerForm = document.getElementById("registerForm");

// Toggle to Register
if (showRegister) {
  showRegister.addEventListener("click", function (e) {
    e.preventDefault();
    loginForm.style.display = "none";
    registerSection.style.display = "block";
  });
}

// Toggle to Login
if (showLogin) {
  showLogin.addEventListener("click", function (e) {
    e.preventDefault();
    registerSection.style.display = "none";
    loginForm.style.display = "block";
  });
}

// Login handler
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Login attempt started");

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log("Email:", email);
    console.log("API_BASE:", API_BASE);

    try {
      const response = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json();

      if (result.success) {
        localStorage.setItem("userEmail", email);
        localStorage.setItem("userPassword", password);
        // Fix: Change from "dashboard" to "dashboard.html"
        window.location.href = "dashboard.html";
      } else {
        alert("Login failed: " + (result.message || "Invalid credentials"));
      }
    } catch (err) {
      alert("Connection error: " + err.message);
    }
  });
}

// Register handler
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;
    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const result = await response.json();
      if (result.success) {
        alert("Registration successful! Please sign in.");
        registerSection.style.display = "none";
        loginForm.style.display = "block";
      } else {
        alert("Registration failed: " + (result.message || "Try again"));
      }
    } catch (err) {
      alert("Connection error: " + err.message);
    }
  });
}
