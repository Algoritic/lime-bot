from decouple import config
import os

from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = config("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = config("AZURE_OPENAI_ENDPOINT")

model = AzureChatOpenAI(
    openai_api_version=config("AZURE_OPENAI_API_VERSION"),
    azure_deployment=config("AZURE_OPENAI_DEPLOYMENT"),
)

message = HumanMessage(
    content="Translate this sentence from English to French. I love programming."
)
response = model([message]).content
print(response)
