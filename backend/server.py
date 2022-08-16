import cv2
from fastapi import FastAPI, File, UploadFile
import tempfile
import uvicorn
import fastdeploy as fd

app = FastAPI()

@app.post("/image/")
async def get_image(file: UploadFile = File(...)):
    # 接收图片
    img = await file.read()
    tempfileName = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    tempfileName.write(img)
    tempfileName.close()

    img = cv2.imread(tempfileName.name)
    model = fd.vision.classification.PaddleClasModel(
                            model_file = 'inference/inference.pdmodel',
                            params_file = 'inference/inference.pdiparams',
                            config_file = 'inference.yml')
    result = model.predict(img)
    labelId = result.label_ids[0]
    with open("dataset/labels_chinese.txt", 'r', encoding="utf-8") as o:
        labelmap = o.readlines()
    label = labelmap[labelId].replace('\n', '')

    if label == '健康叶片':
        status = 'primary'
    else:
        status = 'warn'
        
    return {"disease": label, "status": status}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)