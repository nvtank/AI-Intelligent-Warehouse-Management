import { describe, expect, it, vi } from "vitest";
import { ApiError, getHealth } from "./client";

describe("API client", () => {
  it("reads the health response and passes cancellation to fetch", async () => {
    const body = { status: "ok", service: "mapflow-api", version: "0.1.0", simulation: true };
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify(body)));
    vi.stubGlobal("fetch", fetch);
    const controller = new AbortController();
    await expect(getHealth(controller.signal)).resolves.toEqual(body);
    expect(fetch).toHaveBeenCalledWith(expect.stringMatching(/\/health$/), {
      signal: controller.signal,
      headers: { Accept: "application/json" },
    });
  });

  it("preserves the API error code and message", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      code: "DATABASE_UNAVAILABLE", message: "Chưa kết nối được PostgreSQL.", details: null,
    }), { status: 503 })));
    await expect(getHealth()).rejects.toMatchObject({
      name: "ApiError", status: 503, code: "DATABASE_UNAVAILABLE",
      message: "Chưa kết nối được PostgreSQL.",
    });
  });

  it("handles a non-JSON error from a proxy", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("Bad gateway", { status: 502 })));
    await expect(getHealth()).rejects.toBeInstanceOf(ApiError);
    await expect(getHealth()).rejects.toMatchObject({ status: 502, code: "HTTP_ERROR" });
  });

  it("surfaces connection failures for the error state", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Network failure")));
    await expect(getHealth()).rejects.toThrow("Network failure");
  });
});
