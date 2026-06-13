import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Student API")

with open("mock_students.json") as f:
    students: List[dict] = json.load(f)


class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: str
    major: str


class StudentRequest(BaseModel):
    name: str
    age: int
    grade: str
    major: str


@app.get("/students", response_model=List[Student])
async def get_students():
    return students


@app.get("/students/major/{major}", response_model=List[Student])
async def get_students_by_major(major: str):
    results = [s for s in students if s["major"].lower() == major.lower()]
    if not results:
        raise HTTPException(status_code=404, detail=f"No students found for major '{major}'")
    return results


@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: int):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students", response_model=Student, status_code=201)
async def create_student(payload: StudentRequest):
    new_id = max(s["id"] for s in students) + 1
    student = {"id": new_id, **payload.model_dump()}
    students.append(student)
    return student


@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, payload: StudentRequest):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students[i] = {"id": student_id, **payload.model_dump()}
            return students[i]
    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: int):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students.pop(i)
            return
    raise HTTPException(status_code=404, detail="Student not found")
