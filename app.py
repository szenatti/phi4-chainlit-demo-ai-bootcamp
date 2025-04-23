import chainlit as cl
import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "phi4"

@cl.on_message
async def main(message: cl.Message):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": message.content}],
                "stream": False,
            },
            timeout=60,
        )
    data = resp.json()
    await cl.Message(content=data["message"]["content"]).send()