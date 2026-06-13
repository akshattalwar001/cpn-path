# HTTP Status Codes

## 2xx Success
| Code | Name | Use When |
|------|------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates a resource |
| 204 | No Content | Successful DELETE with no body |

## 4xx Client Errors
| Code | Name | Use When |
|------|------|----------|
| 400 | Bad Request | Invalid input or malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error (FastAPI default) |

## 5xx Server Errors
| Code | Name | Use When |
|------|------|----------|
| 500 | Internal Server Error | Unexpected server-side failure |
| 503 | Service Unavailable | Downstream dependency is down |
