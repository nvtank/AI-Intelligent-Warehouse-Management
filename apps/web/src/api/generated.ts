// Generated from docs/openapi.json. Do not edit by hand.
// Run: npm run types:generate
export interface Schemas {
  "HealthResponse": { "status": "ok"; "service": "mapflow-api"; "version": "0.1.0"; "simulation": true; };
  "ReadinessResponse": { "status": "ready"; "database": "ok"; "simulation": true; };
  "ErrorResponse": { "code": string; "message": string; "details": { [key: string]: unknown; } | null; };
}

export interface Operations {
  "get_health": { responses: {
    200: Schemas["HealthResponse"];
  } };
  "get_readiness": { responses: {
    200: Schemas["ReadinessResponse"];
    503: Schemas["ErrorResponse"];
  } };
}
