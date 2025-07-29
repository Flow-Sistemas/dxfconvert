from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from converter import convert_dxf_to_geojson
import requests
import uuid
import os

app = FastAPI()

class ConversionRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "API de conversão DXF para GeoJSON"}

@app.post("/convert")
def convert(data: ConversionRequest):
    try:
        file_id = str(uuid.uuid4())
        temp_path = f"/tmp/{file_id}.dxf"

        # Faz download do arquivo DXF
        r = requests.get(data.url)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail="Erro ao baixar o arquivo DXF.")
        with open(temp_path, "wb") as f:
            f.write(r.content)

        # Converte para GeoJSON como objeto (não salva em arquivo)
        geojson_data = convert_dxf_to_geojson(temp_path)

        # Apaga o arquivo temporário
        os.remove(temp_path)

        return geojson_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
