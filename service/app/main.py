import uvicorn
from fastapi import FastAPI
import json
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

@app.get("/filters/")
async def root():
  return schema.ListFilters()

@app.get("/filter/{dsid}/")
async def read_item(dsid: str):
  return schema.GetFilter(dsid)

@app.put("/filter/{dsid}/{filter}/")
async def update_item(dsid: str, filter: str):
  return schema.SetFilter(dsid, json.loads(filter))
