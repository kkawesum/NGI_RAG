import axios from "axios";

let csrfToken = "";

export const getCSRFToken = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/chatbot/csrf/", { withCredentials: true });
    csrfToken = response.data.csrfToken;
    axios.defaults.headers.common["X-CSRFToken"] = csrfToken; // Store globally
    console.log("CSRF Token Fetched:", csrfToken);
  } catch (error) {
    console.error("CSRF Token Fetch Error:", error);
  }
};

// Fetch CSRF token when app starts
getCSRFToken();
