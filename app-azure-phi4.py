import os
import chainlit as cl
from azure.ai.inference.aio import ChatCompletionsClient       # async client
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Make sure this URL ends in “/models”
endpoint    = os.getenv("API_ENDPOINT")                        # e.g. https://<your-resource>.services.ai.azure.com/models
model_name  = os.getenv("MODEL_NAME", "Phi-4")                 # must exactly match your deployed model
credential  = AzureKeyCredential(os.getenv("API_KEY"))

@cl.on_message
async def main(message: cl.Message):
    async with ChatCompletionsClient(
        endpoint=endpoint,
        credential=credential,
        model=model_name,
    ) as client:
        # It’s best practice to kick things off with a system message,
        # but you can omit it if you really just want raw user content.
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content=message.content)
        ]
        response = await client.complete(
            messages=messages,
            stream=False,
        )

    # send the assistant’s reply back into Chainlit
    await cl.Message(content=response.choices[0].message.content).send()