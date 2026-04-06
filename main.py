from fastapi import FastAPI
import uvicorn
from models.show import Show
from models.addition import Addition

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"message": "Hari ni hari selasa"}

# POST endpoint
@app.post("/show")
def show_value(item: Show):
    return {
        "message": f"Name: {item.name}, Value: {item.value}"
    }

@app.post("/addition")
def addition(item: Addition):
    return {
        "message": f"Addition: {item.a} + {item.b} = {item.a + item.b}"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
