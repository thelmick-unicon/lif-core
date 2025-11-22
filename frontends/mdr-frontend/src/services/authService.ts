import api from "./api";

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface UserDetails {
  username: string;
  firstname: string;
  lastname: string;
  identifier: string;
  identifier_type: string;
  identifier_type_enum: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  user: UserDetails;
  access_token: string;
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
}

class AuthService {
  private readonly ACCESS_TOKEN_KEY = "access_token";
  private readonly REFRESH_TOKEN_KEY = "refresh_token";
  private readonly USER_KEY = "auth_user";

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>("/login", credentials);

    const loginData = response.data;
    this.setTokens(loginData.access_token, loginData.refresh_token);
    this.setCurrentUser(loginData.user);

    return loginData;
  }

  async logout(): Promise<void> {
    try {
      await api.post("/logout");
    } catch (error) {
      console.warn("Logout request failed:", error);
    }
    this.clearTokens();
  }

  async refreshToken(): Promise<boolean> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      console.warn("No refresh token found, unable to refresh user session.");
      this.clearTokens();
      return false;
    }

    try {
      const response = await api.post<RefreshTokenResponse>("/refresh-token", {
        refresh_token: refreshToken,
      });
      console.info("Successfully refreshed the user session");
      this.setAccessToken(response.data.access_token);
      return true;
    } catch (error) {
      console.warn("Token refresh failed:", error);
      this.clearTokens();
      return false;
    }
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  setAccessToken(token: string): void {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, token);
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }

  setTokens(accessToken: string, refreshToken: string): void {
    this.setAccessToken(accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  clearTokens(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    delete api.defaults.headers.common["Authorization"];
  }

  isAuthenticated(): boolean {
    const token = this.getAccessToken();
    if (!token) return false;

    try {
      // Basic token expiry check - decode JWT payload
      const payload = JSON.parse(atob(token.split(".")[1]));
      const currentTime = Date.now() / 1000;
      return payload.exp > currentTime;
    } catch {
      return false;
    }
  }

  getCurrentUser(): UserDetails | null {
    const userStr = localStorage.getItem(this.USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  }

  setCurrentUser(user: UserDetails): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  initializeAuth(): void {
    const token = this.getAccessToken();
    if (token && this.isAuthenticated()) {
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      this.clearTokens();
    }
  }
}

export default new AuthService();
