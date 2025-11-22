import axios from "axios";
import authService from "./authService";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  // You can add headers or other config here if needed
});

// Add a response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      console.warn("Received a 401 error. Trying to refresh the user session");
      // This may happen synchronously with a different request, which is OK - 
      // the last refresh cycle to complete will be the one to save in local 
      // storage for subsequent requests.

      try {
        // Import here to avoid circular dependency
        const authService = (await import("./authService")).default;
        const refreshed = await authService.refreshToken();

        if (refreshed) {
          // Retry the original request with the new token
          originalRequest.headers["Authorization"] = `Bearer ${authService.getAccessToken()}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        console.error("Token refresh failed, redirecting to login");
        authService.clearTokens();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;
