/* Sunlit Credential data boundary: backend data is explicit, token-scoped, and never silently mocked as real care information. */
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1").replace(/\/$/, "");

export type ApiResult<T> = { data?: T; error?: string };

export const api = {
  baseUrl: API_BASE_URL,
  token: () => localStorage.getItem("vetkonnect_access_token"),
  async request<T>(path: string, init: RequestInit = {}): Promise<ApiResult<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${path}`, {
        ...init,
        headers: {
          "Content-Type": "application/json",
          ...(this.token() ? { Authorization: `Bearer ${this.token()}` } : {}),
          ...(init.headers ?? {}),
        },
      });
      const payload = await response.json().catch(() => undefined) as { error?: { message?: string } } | T | undefined;
      if (!response.ok) {
        const message = payload && typeof payload === "object" && "error" in payload ? payload.error?.message : undefined;
        return { error: message ?? `Request unavailable (${response.status})` };
      }
      return { data: payload as T };
    } catch {
      return { error: "VetKonnect could not reach the secure care service." };
    }
  },
  login: (email: string, password: string) => api.request<{ access: string; refresh: string }>("/auth/login/", { method: "POST", body: JSON.stringify({ email, password }) }),
  register: (payload: { email: string; phone_number?: string; first_name: string; last_name: string; password: string }) => api.request<{ status: "verification_pending"; email: string; expires_in_minutes: number }>("/auth/register/", { method: "POST", body: JSON.stringify(payload) }),
  verifyEmail: (email: string, code: string) => api.request<{ access: string; refresh: string }>("/auth/verify-email/", { method: "POST", body: JSON.stringify({ email, code }) }),
  resendEmailVerification: (email: string) => api.request<{ status: "verification_pending"; retry_after_seconds?: number }>("/auth/verify-email/resend/", { method: "POST", body: JSON.stringify({ email }) }),
  professionalDirectory: () => api.request<unknown[]>("/professionals/professionals/"),
  marketplace: () => api.request<unknown[]>("/marketplace/products/"),
  notifications: () => api.request<unknown[]>("/notifications/"),
  badgePlans: () => api.request<unknown[]>("/billing/badge-plans/"),
};
