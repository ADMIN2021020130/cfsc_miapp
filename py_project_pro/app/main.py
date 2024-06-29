import sys
from pathlib import Path

# 将项目根目录添加到 Python 模块搜索路径中
sys.path.append(str(Path(__file__).resolve().parent.parent))
from fastapi import FastAPI
from app.api.booking import router as booking_router
from app.api.inquiry import router as inquiry_router

app = FastAPI()

app.include_router(booking_router,  tags=["booking"])
app.include_router(inquiry_router, tags=["inquiry"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='app.main:app', host="0.0.0.0", port=8080, reload=True)