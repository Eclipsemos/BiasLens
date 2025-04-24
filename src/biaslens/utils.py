from google import genai

class LLMClient:
    # This class provides methods to interact with the Google Gemini LLM API.

    def __init__(self, LLM_API_KEY, LLM_MODEL_NAME):
        self.client = genai.Client(api_key=LLM_API_KEY)
        self.chat = self.client.chats.create(model=LLM_MODEL_NAME)


    def read_content(self, pre_prompt, content):

        prompt = pre_prompt + "\n" + content
        response = self.chat.send_message(prompt)

        return response.text
        
    def response(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text