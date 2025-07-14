from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from app.operation.chat import get_ollama_response
from app.schemas import PromptRequest

router = APIRouter(prefix="/ollama", tags=["Ollama Chat"])

@router.post("/chat", status_code=status.HTTP_201_CREATED)
async def chat_stream(prompt_req: PromptRequest):
    return StreamingResponse(
        get_ollama_response(prompt_req.prompt, prompt_req.model),
        media_type="text/plain"
    )
