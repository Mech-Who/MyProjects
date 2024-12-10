from fastapi import FastAPI

people = FastAPI()

@people.get("/")
def list_all():
    return {"people": "root"}
