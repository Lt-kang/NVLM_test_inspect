from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

import json

router = APIRouter()

from src.get_user_dir import get_user_dir




@router.get("/problem/{problem_num}", response_class=HTMLResponse)
async def main(request: Request, problem_num: str):
    user_id = request.client.host

    if int(problem_num) == -1:
        return JSONResponse({}, status_code=404)

    user_base_dir = get_user_dir(user_id)

    with open(user_base_dir / "file_index.json", "r", encoding="utf-8") as f:
        file_index = json.load(f)

    file_index_keys = sorted(list(file_index.keys()), key=lambda x: int(x))

    file_index_min = int(file_index_keys[0])
    file_index_max = int(file_index_keys[-1])

    if file_index_min > int(problem_num) or int(problem_num) > file_index_max:
        return JSONResponse({"error": "Invalid ID"}, status_code=404)
    
    target_index = file_index[str(problem_num)]

    json_files = [file for file in user_base_dir.rglob("*.json") if file.name != "file_index.json"]
    if not json_files:
        return JSONResponse({"message": "json 파일이 존재하지 않습니다."}, status_code=404)

    json_file = json_files[0]
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    target_data = data['data'][target_index]
    return JSONResponse(target_data, status_code=200)

