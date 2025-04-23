from google import genai
from cfg import LLM_API_KEY, LLM_MODEL_NAME

class LLMUtils:
    """
    This class provides methods to interact with the Google Gemini LLM API.
    """

    def __init__(self):
        self.LLM_API_KEY = LLM_API_KEY
        self.LLM_MODEL_NAME = LLM_MODEL_NAME
        self.client = genai.Client(api_key=self.LLM_API_KEY)
    

    def page_information_extractor(self, page_content):
        # This function sends the page content to the LLM API for information extraction.

        prompt = (
            f"Based on the following news article, extract and return the following information in JSON format:\n"
            f"- The article's (possible) title\n"
            f"- The list of author(s)\n"
            f"- The primary news institution responsible for publication\n"
            f"- The news category (e.g., Politics, Technology, Sports)\n"
            f"- The time or date of the events (use publication time if unknown)\n"
            f"- A concise abstract (1–3 sentence summary)\n"
            f"- The list of main entities covered (e.g., individuals, organizations, or groups)\n\n"
            f"For any unknown information, use [UNK] as a placeholder. Respond only with a JSON object in the following format:\n"
            f"{{\"title\": \"xxx\", \"authors\": [\"xxx\", \"xxx\", ...], \"institution\": \"xxx\", \"category\": \"xxx\", \"time\": \"xxx\", \"abstract\": \"xxx\", \"entities\": [\"xxx\", \"xxx\", ...]}}\n\n"
            f"Here is the news article:\n{page_content}"
        )

        response = client.models.generate_content(
            model=self.LLM_MODEL_NAME,
            contents=[prompt]
        )

        return response.text