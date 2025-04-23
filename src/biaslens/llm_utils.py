from google import genai
from cfg import LLM_API_KEY, LLM_MODEL_NAME

class LLMUtils:
    # This class provides methods to interact with the Google Gemini LLM API.

    def __init__(self, page_gross_text):
        self.LLM_API_KEY = LLM_API_KEY
        self.LLM_MODEL_NAME = LLM_MODEL_NAME

        self.client = genai.Client(api_key=self.LLM_API_KEY)
        self.chat = self.client.chats.create(model=self.LLM_MODEL_NAME)
        
        self._read_page(page_gross_text)



    def _read_page(self, page_gross_text):
        # This function reads the page content as a global context.

        prompt = (
            "Please read the following article from a news website carefully and retain its information and details. "
            "Please hold on — I'll ask you questions about it shortly. Here is the news article:\n"
            f"{page_gross_text}"
        )

        response = self.chat.send_message(prompt)
        print(f"Reading page content...\nResponse: {response.text}")

        return response.text

    

    def page_information_extractor(self):
        # This function extracts information from the page content.

        prompt = (
            "Good! Now based on the news article provided above, extract and return the following information in JSON format:\n"
            "- The article's (possible) title\n"
            "- The list of author(s)\n"
            "- The primary news institution responsible for publication\n"
            "- The news category (e.g., Politics, Technology, Sports)\n"
            "- The time or date of the events (use publication time if unknown)\n"
            "- A concise abstract (1–3 sentence summary)\n"
            "- The list of main entities covered (e.g., individuals, organizations, or groups)\n\n"
            "For any unknown information, leave it empty (\"\" or []) as a placeholder. Respond only with a JSON object in the following format:\n"
            "{\"title\": \"xxx\", \"authors\": [\"xxx\", \"xxx\", ...], \"institution\": \"xxx\", \"category\": \"xxx\", \"time\": \"xxx\", \"abstract\": \"xxx\", \"entities\": [\"xxx\", \"xxx\", ...]}\n"
        )

        response = self.chat.send_message(prompt)
        print(f"Extracting information...\nResponse:\n {response.text}")

        return response.text


    def page_claims_extractor(self):
        # This function extracts claims from the page content.

        prompt = (
            "Excellent! Now given the news article above, identify and extract two or three different key claims presented within it. "
            "A claim is any statement that can be evaluated as true or false, including opinions, alleged facts, assertions, or conclusions. "
            "Summarize each claim clearly and concisely. "
            "After listing the claims, generate a corresponding search query for each one. These queries should be designed to help verify the truthfulness of each claim by searching relevant information online.\n"
            "Return your response as a JSON object in the following format:\n"
            "{\"claims\": [\"claim1\", \"claim2\", ...], \"queries\": [\"query1\", \"query2\", ...]}\n"
        )

        response = self.chat.send_message(prompt)
        print(f"Extracting claims...\nResponse:\n {response.text}")
        return response.text
        