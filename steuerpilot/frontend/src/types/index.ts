export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "MANDANT" | "STEUERBERATER" | "ADMIN";
  tenant_id: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role?: string;
  tenant_name?: string;
}
