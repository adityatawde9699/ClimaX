# ClimaX API Documentation

The ClimaX API is built with FastAPI and strictly adheres to REST principles and OpenAPI 3.1 standards.

## 1. Interactive API Explorers

When running the backend locally (`npm run dev:api` or `uvicorn main:app --reload`):
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON Spec**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 2. Global Standards & Protocols

- **Base URL**: `/api/v1`
- **Transport**: HTTPS mandatory in production; HTTP allowed on localhost.
- **Data Format**: `application/json` with UTC ISO-8601 timestamps (`YYYY-MM-DDTHH:MM:SSZ`).
- **Authentication**: `Authorization: Bearer <jwt_token>` header for authorized municipal and researcher endpoints.

---

## 3. Standard Response Formats

### Single Entity Response (`ApiResponse<T>`)
```json
{
  "success": true,
  "data": {
    "id": "rep-4c28f11a",
    "tier": "OBSERVED",
    "status": "SUBMITTED"
  },
  "message": "Citizen report submitted successfully"
}
```

### Paginated Collection Response (`PaginatedResponse<T>`)
```json
{
  "success": true,
  "data": [...],
  "total": 1420,
  "page": 1,
  "per_page": 20,
  "total_pages": 71
}
```

### Error Response Envelope
```json
{
  "success": false,
  "error": {
    "type": "EntityNotFoundException",
    "message": "Incident with ID inc-9921 not found",
    "details": {}
  }
}
```
