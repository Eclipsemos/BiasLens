import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from google.generativeai import types
from .prompt_lib import prompt_lib


class QueryWebRetriever:
    # This class provides methods to retrieve information from the web using Google Custom Search API.

    def __init__(self, LLM_API_KEY, LLM_MODEL_NAME, SEARCH_ENGINE_ID, SEARCH_API_KEY):
        genai.configure(api_key=LLM_API_KEY)
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
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()

            text = soup.get_text(separator=' ', strip=True)
            characters = max_content_length * 4
            text = text[:characters]
            return text
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return None


    def _get_web_summary(self, content, query, max_summary_length=500):
        try:
            prompt = prompt_lib["search_summary_prompt"].format(
                query=query,
                max_summary_length=max_summary_length,
                content=content
            )
            model = genai.GenerativeModel(self.llm_model_name)
            response = model.generate_content(prompt)
            return response.text


        except Exception as e:
            print(f"Error during summarization: {e}")
            return None


    def get_retrieval_results(self, query, search_depth=5):
        results = []
        searched_items = self._search(query, search_depth)
        for item in searched_items:
            title = item.get('title')
            displayLink = item.get('displayLink')
            link = item.get('link')
            content = self._get_web_content(link)
            if content:
                summary = self._get_web_summary(content, query)
            else:
                summary = title + '\n' + item.get('snippet', '')
            results.append({
                'title': title,
                'summary': summary,
                'displayLink': displayLink,
                'link': link
            })
        return results

