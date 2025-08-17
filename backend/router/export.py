from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Form

from pathlib import Path
import json

from src.get_user_dir import get_user_dir

router = APIRouter()


@router.get("/export", response_class=FileResponse)
async def export_json(request: Request):
    try:
        user_id = request.client.host
        user_base_dir = get_user_dir(user_id)

        json_files = [file for file in user_base_dir.rglob("*.json") if file.name != "file_index.json"]
        if not json_files:
            return JSONResponse({"message": "json 파일이 존재하지 않습니다."}, status_code=404)
        

        headers = {
            "Content-Disposition": f'attachment; filename="{json_files[0].name}"',
            # 브라우저에서 파일명 노출 필요 시(CORS 환경)
            "Access-Control-Expose-Headers": "Content-Disposition",
        }

        return FileResponse(
            json_files[0],
            media_type="application/json",
            headers=headers
        )

    except Exception as e:
        return JSONResponse({"message": f"다운로드 실패: {str(e)}"}, status_code=400)
    

