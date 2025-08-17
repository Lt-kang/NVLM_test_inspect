'''
upload_file
'''
'''
register_user
create_user_dir
'''

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pathlib import Path
import json

from src.get_user_dir import get_user_dir


router = APIRouter()



from fastapi import UploadFile, File


def split_data(json_path:str) -> dict:
    json_path = Path(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data_list = data["data"]

    problem_mapping = {str(obj['problem_num']): idx for idx, obj in enumerate(data_list)}
    return problem_mapping


'''
1. create_user_dir
2. create_file_index.json
3. file preprocessing
'''
@router.post("/load", response_class=JSONResponse)
async def load_file(
    request: Request,
    # user_folder: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        user_id = request.client.host

        user_base_dir = Path(get_user_dir(user_id, init=True))

       
        '''
        upload file을 server local에 저장
        '''
        saved_files = []
        filename = file.filename
        if filename.lower().endswith(".json"):
            file_path = user_base_dir / filename
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            saved_files.append(filename)

        if not saved_files:
            print("저장된 파일이 없습니다. png 또는 html 파일만 허용됩니다.")
            return JSONResponse({"message": "저장된 파일이 없습니다. png 또는 html 파일만 허용됩니다."}, status_code=400)
        

        '''
        파일을 전부 server에 저장하였다면
        전처리를 시작함.
        이는 이후 작업시 load를 빨리 하기 위함에 있음.
        '''
        problem_mapping = split_data(file_path)
        with open(user_base_dir / "file_index.json", "w", encoding="utf-8") as f:
            json.dump(problem_mapping, f, ensure_ascii=False, indent=4)

        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        
        return JSONResponse({"message": "upload success", 
                             "json_data": json_data,
                             "problem_mapping": sorted(list(problem_mapping.keys()), key=lambda x: int(x))}, status_code=200)
    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"upload failed: {str(e)}"}, status_code=400)


