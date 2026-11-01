import type { Operations, Schemas } from "./generated";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly details: Schemas["ErrorResponse"]["details"],
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function getHealth(
  signal?: AbortSignal,
): Promise<Operations["get_health"]["responses"][200]> {
  const baseUrl = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000").replace(/\/$/, "");
  const response = await fetch(`${baseUrl}/health`, {
    signal,
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    if (
      typeof body === "object" && body !== null &&
      "code" in body && typeof body.code === "string" &&
      "message" in body && typeof body.message === "string"
    ) {
      throw new ApiError(response.status, body.code, body.message, null);
    }
    throw new ApiError(response.status, "HTTP_ERROR", "Không thể kết nối API.", null);
  }
  return response.json();
}
