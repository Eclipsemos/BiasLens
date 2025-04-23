from llm_utils import LLMUtils
from article import Article
import json

        
class BiasLens:
    # This class provides methods to analyze bias, fact-check, retrieve opposite perspectives and summaries from news articles.

    def __init__(self, req):
        self.req = req
        page_gross_text = self.req.get("page_gross_text")
        
        self.llm_utils = LLMUtils(page_gross_text)
        
        self.article = self._build_article(page_gross_text)

        print(self.article.__dict__)


    def _build_article(self, page_gross_text):
        article = Article(page_gross_text)
        
        # Extract information from the article using LLM
        info = self.llm_utils.page_information_extractor()
        info = info.strip().removeprefix("```json").removesuffix("```").strip()
        info = json.loads(info)
        article.setup_info(**info)


        # Extract claims from the article using LLM
        claims = self.llm_utils.page_claims_extractor()
        claims = claims.strip().removeprefix("```json").removesuffix("```").strip()
        claims = json.loads(claims)
        article.setup_claims(**claims)

        
        
        return article