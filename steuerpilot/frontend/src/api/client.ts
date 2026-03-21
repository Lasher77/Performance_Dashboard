import { useAuthStore } from "../store/auth";
import type { LoginRequest, RegisterRequest, TokenResponse, User } from "../types";

const BASE_URL = "/api";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = useAuthStore.getState().accessToken;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Try refresh
    const refreshToken = useAuthStore.getState().refreshToken;
    if (refreshToken) {
      try {
        const refreshResponse = await fetch(`${BASE_URL}/auth/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
        if (refreshResponse.ok) {
          const tokens: TokenResponse = await refreshResponse.json();
          useAuthStore.getState().setTokens(tokens.access_token, tokens.refresh_token);

          // Retry original request
          headers["Authorization"] = `Bearer ${tokens.access_token}`;
          const retryResponse = await fetch(`${BASE_URL}${path}`, { ...options, headers });
          if (!retryResponse.ok) {
            throw new Error(`HTTP ${retryResponse.status}`);
          }
          return retryResponse.json();
        }
      } catch {
        useAuthStore.getState().logout();
      }
    }
    useAuthStore.getState().logout();
    throw new Error("Nicht autorisiert");
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unbekannter Fehler" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  auth: {
    register: (data: RegisterRequest) =>
      request<User>("/auth/register", { method: "POST", body: JSON.stringify(data) }),

    login: (data: LoginRequest) =>
      request<TokenResponse>("/auth/login", { method: "POST", body: JSON.stringify(data) }),

    me: () => request<User>("/auth/me"),
  },

  health: () => request<{ status: string }>("/health"),
};
