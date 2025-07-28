from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from automation_async import run_campaigns
import os

load_dotenv()
app = FastAPI()

@app.post("/automation")
async def automation_handler(request: Request):
    payload = await request.json()

    secret = request.headers.get("Authorization")
    if secret != f"Bearer {os.getenv('AUTOMATION_SECRET')}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    campaign_ids = payload.get("campaign_ids", [])
    results = await run_campaigns(campaign_ids)
    return { "status": "done", "processed": results }
