#!/usr/bin/env python3
"""_summary_
    File containing boilerplate functions that could be used by the server in it's endpoints_initialised for checking incoming data.
"""

from fastapi import FastAPI, Request
import logging

app = FastAPI()

class Webhook:
    data = []

    logging.basicConfig(level=logging.INFO)

    @app.post("/webhook") # put this in endpoints routes
    async def receive_webhook(request: Request):
        payload = await request.json()

        logging.info(f"Received webhook data: {payload}")
        print(f"payload: {payload}")
        return {"message": "Webhook received", "data": payload}

    @app.get("/")
    async def test():
        return "test"

# test
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
