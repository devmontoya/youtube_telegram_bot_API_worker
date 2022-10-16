import time

from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from worker.utilities_worker import NoVideosFound
from worker.worker import close_driver, get_videos

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return True


@app.get("/request_task_id_get_videos/{channel}")
def pass_channel(channel: str):
    task_id = get_videos.delay(channel).id
    return JSONResponse({"task_id": task_id})


@app.get("/task_id_get_videos/{task_id}")
def task_id_get_videos(task_id: str):
    task_result = AsyncResult(task_id)
    if isinstance(task_result.result, NoVideosFound):
        raise HTTPException(status_code=404, detail=task_result.result.args[0])

    return JSONResponse(
        {"task_result": task_result.result, "task_status": task_result.status}
    )


@app.get("/request_videos/{channel}", response_model=list[list[str]])
def request_videos(channel: str):
    try:
        task = get_videos.delay(channel).get()
    except NoVideosFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return task


@app.on_event("shutdown")
@app.get("/shutdown")
def shutdown_selenium_session():
    close_driver.delay().get()
    return True
