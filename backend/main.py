from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

from evaluator import evaluate, highlight

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔴 MongoDB (अपना नया password डालो)
client = MongoClient("mongodb+srv://Namansoni23:Krati*2302@shorthandpractice.c2ku6fe.mongodb.net/")
db = client["steno"]

users = db["users"]
tests = db["tests"]
results = db["results"]

# -------- MODELS --------
class User(BaseModel):
    name: str
    password: str

class Test(BaseModel):
    id: int
    title: str
    passage: str
    audio: str

class Submit(BaseModel):
    name: str
    user_text: str
    test_id: int

# -------- AUTH --------
@app.post("/signup")
def signup(data: User):
    if users.find_one({"name": data.name}):
        return {"msg": "User exists"}
    users.insert_one(data.dict())
    return {"msg": "Account created"}

@app.post("/login")
def login(data: User):
    u = users.find_one({"name": data.name, "password": data.password})
    if u:
        return {"msg": "success"}
    return {"msg": "invalid"}

# -------- TEST --------
@app.post("/create-test")
def create_test(data: Test):
    tests.insert_one(data.dict())
    return {"msg": "test added"}

@app.get("/tests")
def get_tests():
    return list(tests.find({}, {"_id": 0}))

@app.delete("/delete-test/{id}")
def delete_test(id: int):
    tests.delete_one({"id": int(id)})
    return {"msg": "deleted"}

@app.get("/test/{id}")
def get_test(id: int):
    return tests.find_one({"id": id}, {"_id": 0})

# -------- SUBMIT --------
@app.post("/submit")
def submit(data: Submit):
    t = tests.find_one({"id": data.test_id})
    master = t["passage"]

    result = evaluate(master, data.user_text)
    result["highlight"] = highlight(master, data.user_text)

    results.insert_one({
        "name": data.name,
        "test_id": data.test_id,
        "result": result
    })

    return result

# -------- ADMIN --------
@app.get("/all-results")
def all_results():
    return list(results.find({}, {"_id": 0}))

@app.get("/users")
def get_users():
    return list(users.find({}, {"_id": 0}))
