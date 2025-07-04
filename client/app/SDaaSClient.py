import asyncio
import time
import httpx
import json

class SDaaSClient:
  def __init__(self, name = None):
    self.name = name
    # Assuming your FastAPI app is running on http://127.0.0.1:8000
    self.base_url = "http://127.0.0.1:8411"

  async def GetDatasets(self):
    async with httpx.AsyncClient() as client:
      response = await client.get(f"{self.base_url}/datasets/")
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.json()

  async def GetDataset(self, ds_id: str):
    async with httpx.AsyncClient() as client:
      response = await client.get(f"{self.base_url}/dataset/{ds_id}/")
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.json()

  async def GetFilters(self):
    async with httpx.AsyncClient() as client:
      response = await client.get(f"{self.base_url}/filters/")
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.json()

  async def GetFilter(self, ds_id: str):
    async with httpx.AsyncClient() as client:
      response = await client.get(f"{self.base_url}/filter/{ds_id}/")
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.json()

  async def SetFilter(self, ds_id: str, schema):
    async with httpx.AsyncClient() as client:
      schema_str = json.dumps(schema)
      response = await client.put(f"{self.base_url}/filter/{ds_id}/{schema_str}/")
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.json()


