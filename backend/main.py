from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from evaluator import evaluate

app = FastAPI()

# MongoDB
client = MongoClient("YOUR_MONGO_URL")
db = client["steno"]
tests = db["tests"]
results = db["results"]

class SubmitData(BaseModel):
    name: str
    user: str
    test_id: int

# create test (admin use)
@app.post("/create-test")
def create_test(data: dict):
    tests.insert_one(data)
    return {"msg": "test created"}

# get test
@app.get("/test/{id}")
def get_test(id: int):
    t = tests.find_one({"id": id}, {"_id": 0})
    return t

# submit
@app.post("/submit")
def submit(data: SubmitData):

    t = tests.find_one({"id": data.test_id})

    master = t["passage"]

    result = evaluate(master, data.user)

    results.insert_one({
        "name": data.name,
        "test_id": data.test_id,
        "result": result
    })

    return result
