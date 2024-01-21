from decouple import config
from openai import AzureOpenAI

class AzureOpenAIChatClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=config("AZURE_OPENAI_API_KEY"),
            api_version=config("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=config("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=config("AZURE_OPENAI_DEPLOYMENT")
        )

    def get_chat_response(self, prompt):
        completion = self.client.chat.completions.create(
            model=config("MODEL_NAME"),  # e.g. gpt-35-instant
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return completion.choices[0].message.content

# Usage
if __name__ == "__main__":
    chat_client = AzureOpenAIChatClient()
    joke = chat_client.get_chat_response("Tell me a joke about a penguin sitting on a fridge.")
    print(joke)
