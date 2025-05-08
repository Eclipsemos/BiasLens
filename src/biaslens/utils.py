from google import genai
import requests



class LLMChat:
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



class QueryWebRetriever:
    # This class provides methods to retrieve information from the web using Google Custom Search API.

    def __init__(self, LLM_API_KEY, LLM_MODEL_NAME, SEARCH_ENGINE_ID, SEARCH_API_KEY):
        self.client = genai.Client(api_key=LLM_API_KEY)
        self.llm_model_name = LLM_MODEL_NAME
        self.search_engine_id = SEARCH_ENGINE_ID
        self.search_api_key = SEARCH_API_KEY


    def _search(self, query, search_depth=10):
        service_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': self.search_api_key,
            'cx': self.search_engine_id,
            'num': search_depth
        }
        try:
            response = requests.get(service_url, params=params)
            response.raise_for_status()
            results = response.json()
            if 'items' in results:
                return results['items']
            else:
                print("No items found in the search results.")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error during search: {e}")
            return []


    def _get_web_content(self, url, max_content_length=50000):
        pass

    def _get_web_summary(self, content, max_summary_length=500):
        pass

    def get_retrieval_results(self, query, search_depth=10):
        searched_items = self._search(query, search_depth)
        for item in searched_items:
            print(item)
    
