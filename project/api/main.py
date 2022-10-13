import time

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from worker.worker import close_driver, get_videos

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return True


@app.get("/channel/{channel}")
def pass_channel(channel: str):
    task_id = get_videos.delay(channel).id
    return JSONResponse({"task_id": task_id})


@app.get("/task_id_get_videos/{task_id}")
def task_id_get_videos(task_id):
    task_result = AsyncResult(task_id)
    return JSONResponse(
        {"task_result": task_result.result, "task_status": task_result.status}
    )


@app.on_event("shutdown")
@app.get("/shutdown")
def shutdown_selenium_session():
    task_id = str(close_driver.delay())
    time.sleep(5)
    while AsyncResult(task_id).status != "SUCCESS":
        time.sleep(1)

    return True
