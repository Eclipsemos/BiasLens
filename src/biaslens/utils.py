import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from google.generativeai import types
from html import unescape

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
    
    def _get_reddit_content(self, url: str, headers, max_depth = 2) -> str:
        json_url = url.rstrip("/") + "/.json"
        r = requests.get(json_url, params={"raw_json": 1}, headers=headers, timeout=(3, 7))
        r.raise_for_status()

        post_listing, comment_listing = r.json()
        post  = post_listing["data"]["children"][0]["data"]
        lines = []

        def html_to_text(html: str) -> str:
            return BeautifulSoup(unescape(html), "html.parser").get_text(" ", strip=True)

        title = post["title"]
        body  = post.get("selftext_html") or ""
        lines.append(f"### {title}\n")
        if body:
            lines.append(html_to_text(body) + "\n")

        def walk(children, depth=0):
            if depth >= max_depth:
                return
            for item in children:
                if item["kind"] != "t1":
                    continue
                data   = item["data"]
                author = data["author"]
                text   = html_to_text(data["body_html"])
                lines.append("  " * depth + f"- u/{author}: {text}")
                if data.get("replies"):
                    walk(data["replies"]["data"]["children"], depth + 1)

        walk(comment_listing["data"]["children"])
        return "\n".join(lines)


    def _get_web_content(self, url, max_content_length=50000):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/json;q=0.9,"
                    "application/xml;q=0.8,*/*;q=0.7"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive"
            }
            if "www.reddit.com" in url:
                text = self._get_reddit_content(url, headers)
            elif "www.newsmax.com" in url or url.endswith(".pdf"): # cannot access
                return None
            else:
                response = requests.get(url, headers=headers, timeout=(3, 7))
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

