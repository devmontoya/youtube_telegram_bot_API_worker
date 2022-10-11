from celery.result import AsyncResult
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from worker.worker import add_channel

app = FastAPI()


@app.get("/{channel}")
def pass_channel(channel: str):
    task_id = add_channel.delay(channel).id
    return JSONResponse({"task_id": task_id})


@app.post("/page")
def pass_channel(channel: str = Body(...)):
    task_id = add_channel.delay(channel).id
    print(channel)
    return JSONResponse({"task_id": task_id})


@app.get("/task_id/{task_id}")
def get_task(task_id):
    task_result = AsyncResult(task_id)
    return JSONResponse(
        {"task_result": task_result.result, "task_status": task_result.status}
    )
