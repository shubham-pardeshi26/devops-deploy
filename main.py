from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
from typing import List, Dict, Any
import json

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    value: float

class LargeResponse(BaseModel):
    items: List[Item]
    count: int

# Mock data generation
def generate_large_data(num_items: int) -> List[Item]:
    return [Item(id=i, name=f"Item {i}", value=random.uniform(10.0, 100.0)) for i in range(num_items)]

# Initialize with some large data
large_data = generate_large_data(1000)

@app.get("/large-data", response_model=LargeResponse)
async def get_large_data():
    """
    Get a large dataset.
    """
    try:
        data = large_data
        return LargeResponse(items=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/filter-large-data", response_model=LargeResponse)
async def filter_large_data(min_value: float, max_value: float):
    """
    Get a filtered large dataset based on value range.
    - min_value: Minimum value for filtering
    - max_value: Maximum value for filtering
    """
    try:
        filtered_data = [item for item in large_data if min_value <= item.value <= max_value]
        return LargeResponse(items=filtered_data, count=len(filtered_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

class DictionaryModel(BaseModel):
    data: Dict[str, Any]

@app.post("/save-json")
async def save_json(dictionary: DictionaryModel):
    """
    Save the provided dictionary as a JSON file in local storage.
    - dictionary: The dictionary to be saved as JSON
    """
    try:
        # Define the path to save the JSON file
        file_path = "saved_data.json"
        
        # Write the dictionary to the JSON file
        with open(file_path, "w") as json_file:
            json.dump(dictionary.data, json_file, indent=4)
        
        return {"message": "Data successfully saved to JSON file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")