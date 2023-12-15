import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Request
from langchain.chat_models import ChatOpenAI
from langserve import add_routes


app = FastAPI()


def verify_secret_key(config: Dict[str, Any], req: Request) -> Dict[str, Any]:
    if req.headers.get("x-secret-key") != os.environ.get("SECRET_KEY"):
        raise HTTPException(status_code=401, detail="Incorrect secret key")

    return config


add_routes(
    app,
    ChatOpenAI(),
    path="/chat",
    per_req_config_modifier=verify_secret_key,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(
        os.getenv("PORT", default=8000)))
