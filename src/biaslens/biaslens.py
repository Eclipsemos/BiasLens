from prompt_lib import prompt_lib
from utils import LLMChat, QueryWebRetriever
import json

        
class BiasLens:
    # This class provides methods to analyze bias, fact-check, retrieve opposite perspectives and summaries from news articles.

    def __init__(
        self,
        req,
        LLM_API_KEY,
        LLM_MODEL_NAME,
        SEARCH_ENGINE_ID,
        SEARCH_API_KEY,
    ):

        self.llm = LLMChat(LLM_API_KEY, LLM_MODEL_NAME)
        self.retriever = QueryWebRetriever(LLM_API_KEY, LLM_MODEL_NAME, SEARCH_ENGINE_ID, SEARCH_API_KEY)

        self.page_gross_text = req.get("page_gross_text")

        self.results = {}


    def _article_reading(self):
        self.llm.read_content(
            prompt_lib["article_reading_prompt"],
            self.page_gross_text
        )


    def _article_pre_analysis(self):
        prompt_queue = [
            "article_information_extract_prompt",
            "article_expressive_intent_extract_prompt"
        ]

        for prompt in prompt_queue:
            res = self.llm.response(prompt_lib[prompt])
            res = res.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            self.results.update(res)
        
        if "opinion" in self.results.get("expressive_intent").lower() or self.results.get("expressive_intent") == "":
            prompt_queue = [
                "op_argument_extract_prompt",
                "op_tendency_extract_prompt"
            ]
        else:
            prompt_queue = [
                "news_argument_extract_prompt",
                "news_tendency_extract_prompt"
            ]
        for prompt in prompt_queue:
            res = self.llm.response(prompt_lib[prompt])
            res = res.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            self.results.update(res)

    
    def _prior_bias_analysis(self):
        # TODO:
        # Analyze the background of the institution.
        # Search online to identify ideological leanings, political affiliations, media type(independent/commercial/government affiliated) and credibility.
        # Provide citations for all findings.
        query = f"\"{self.results.get('institution')}\" credibility reliability"
        self.retriever.get_retrieval_results(query, search_depth=3)


    def _fact_check(self):
        # TODO:
        # Evaluate the accuracy of each alleged fact.
        # Cross-reference with credible online sources and apply logical reasoning.
        # Categorize each fact as Verified, Partly True / Misleading, False, Disputed / Inconclusive, or Unverifiable.
        # Include citations for all supporting information.
        pass

    def _get_opposite_perspective(self):
        # TODO:
        # Identify opposing viewpoints for each opinion expressed in the article.
        # Search online for credible sources presenting counterarguments.
        # Summarize key points and provide citations.
        pass

    def _get_bias_conclusion(self):
        # TODO:
        # Summarize the overall bias of the article.
        # 
        # For opinion content, evaluate based on:
        # - Accuracy of facts
        # - Adequacy of supporting evidence
        # - Logical coherence of arguments
        # - Overall integrity and fairness of the information presented
        #
        # For news reporting, evaluate based on:
        # - Factual accuracy
        # - Presence of guiding or selective framing
        # - Neutrality of language
        # - Overall integrity and balance of the information presented

        pass


    def run(self):

        self._article_reading()
        self._article_pre_analysis()
        self._prior_bias_analysis()
        self._fact_check()
        self._get_opposite_perspective()

        return self.results




        