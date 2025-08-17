from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from router import (
    load,
    export,
    problem
)



app = FastAPI()

app.include_router(problem.router, prefix="/api/v1")
app.include_router(load.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")

'''
get
/api/v1/inspect
/api/v1/extract


post
/api/v1/load
/api/v1/save
'''

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱의 주소
    # allow_origins=["*"],  # 모든 주소 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/health")
async def health_check():
    """API 상태 확인 엔드포인트"""
    return {"status": "healthy", "message": "FastAPI 서버가 정상 작동 중입니다"}


if __name__ == "__main__":
    # uvicorn.run('run_api:app', host="172.127.0.201", port=8000, reload=True)
    uvicorn.run('run_api:app', host="localhost", port=8000, reload=True)

