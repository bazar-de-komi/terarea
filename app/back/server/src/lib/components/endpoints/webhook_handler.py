"""_summary_
    File containing boilerplate functions that could be used by the server in it's endpoints_initialised for checking incoming data.
"""

from fastapi import FastAPI, Request
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    
    logging.info(f"Received webhook data: {payload}")
    
    # process the data or trigger some action here
    
    return {"message": "Webhook received", "data": payload}
