import asyncio
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Kitchen Service")
NUM_COOKS = 1
cook_semaphore = asyncio.Semaphore(NUM_COOKS)

class SmoothieOrder(BaseModel):
    flavor: str

@app.post("/prepare")
async def prepare_smoothie(order: SmoothieOrder):
    try:
        await asyncio.wait_for(cook_semaphore.acquire(), timeout=2.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=503, detail="All cooks are currently busy")

    try:
        # Prepare the smoothie
        await asyncio.sleep(random.uniform(1.5, 2.5))

        return {"status": "done", "flavor": order.flavor}
    finally:
        cook_semaphore.release()