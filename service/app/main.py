import uvicorn
from fastapi import FastAPI
from openschema.openschema import OpenSchema

app = FastAPI()
params = {
  'catalog': './openschema/catalog.json',
  'dataset': 'ATLAS_DR1',
  'port': 8411
}
schema = OpenSchema(params)

@app.get("/datasets/")
async def root():
    return schema.ListDatasets()

@app.get("/dataset/{dsid}/")
async def read_item(dsid: str):
    return schema.GetDataset(dsid)
