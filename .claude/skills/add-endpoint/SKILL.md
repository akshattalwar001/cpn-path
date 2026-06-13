---
name: add-endpoint
description: Creates a new FastAPI endpoint. Use when adding a route, creating an API endpoint, or when the user asks to add a new endpoint to the FastAPI app.
model: claude-sonnet-4-7
allowedTools: Read, Write, Edit, Glob, Grep, Bash
---

When creating a FastAPI endpoint:

1. Ask the user for:
   - HTTP method (GET, POST, PUT, DELETE)
   - Route path (e.g. `/users/{id}`)
   - What the endpoint should do

2. Create the endpoint following this format:

## Request model (if POST/PUT/PATCH)
```python
class ItemRequest(BaseModel):
    field: type
    field: type
```

## Response model
```python
class ItemResponse(BaseModel):
    id: int
    field: type
```

## Route
```python
@router.get("/path/{id}", response_model=ItemResponse)
async def endpoint_name(id: int, db: Session = Depends(get_db)):
    # logic here
    return result
```

## Rules
- Always use `async def`
- Always define a `response_model`
- Use `HTTPException` for error responses with appropriate status codes
- Put request/response models above the route in the same file
- Use dependency injection for db sessions
