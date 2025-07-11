import httpx
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"


async def get_ollama_response(prompt: str, model: str = "llama3:latest"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", OLLAMA_API_URL, json=payload) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        yield chunk
                    except json.JSONDecodeError:
                        continue
