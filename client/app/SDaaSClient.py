import asyncio
import time
import httpx

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

  async def GetDataset(self, item_id: int):
    async with httpx.AsyncClient() as client:
      response = await client.get(f"{self.base_url}/dataset/{item_id}/")
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.json()


