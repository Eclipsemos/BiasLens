from prompt_lib import prompt_lib
from utils import LLMClient
import json

        
class BiasLens:
    # This class provides methods to analyze bias, fact-check, retrieve opposite perspectives and summaries from news articles.

    def __init__(
        self,
        req,
        LLM_API_KEY,
        LLM_MODEL_NAME
    ):

        self.llm = LLMClient(LLM_API_KEY, LLM_MODEL_NAME)
        self.page_gross_text = req.get("page_gross_text")

        self.results = {}

        self.llm.read_content(
            prompt_lib["article_reading_prompt"],
            self.page_gross_text
        )


    def article_pre_analysis(self):
        prompt_queue = [
            "article_information_extract_prompt",
            "article_argument_extract_prompt",
            "article_tendency_extract_prompt"            
        ]

        for prompt in prompt_queue:
            res = self.llm.response(prompt_lib[prompt])
            res = res.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            self.results.update(res)
    




        