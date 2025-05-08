from prompt_lib import prompt_lib
from utils import QueryWebRetriever
import json
from google import genai
from google.genai import types


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
        self.LLM_API_KEY = LLM_API_KEY
        self.LLM_MODEL_NAME = LLM_MODEL_NAME
        self.retriever = QueryWebRetriever(LLM_API_KEY, LLM_MODEL_NAME, SEARCH_ENGINE_ID, SEARCH_API_KEY)
        self.page_gross_text = req.get("page_gross_text")
        self.results = {}


    def article_pre_analysis(self):
        client = genai.Client(api_key=self.LLM_API_KEY)
        article_pre_analyzer = client.chats.create(model=self.LLM_MODEL_NAME)
        

        # read the article
        article_pre_analyzer.send_message(
            prompt_lib["article_reading_prompt"].format(article=self.page_gross_text)
        )

        article_info = {}
        for prompt in [
            "article_information_extract_prompt",
            "article_expressive_intent_extract_prompt"
        ]:
            res = article_pre_analyzer.send_message(prompt_lib[prompt])
            res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            article_info.update(res)
        self.results["article_info"] = article_info
        
        if "opinion" in article_info.get("expressive_intent").lower() or article_info.get("expressive_intent") == "":
            prompt_queue = [
                "op_argument_extract_prompt",
                "op_tendency_extract_prompt"
            ]
        else:
            prompt_queue = [
                "news_argument_extract_prompt",
                "news_tendency_extract_prompt"
            ]
        article_arguments = {}
        for prompt in prompt_queue:
            res = article_pre_analyzer.send_message(prompt_lib[prompt])
            res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            article_arguments.update(res)
        
        self.results["article_arguments"] = article_arguments

        return article_info, article_arguments

    
    def institution_bias_analysis(self):
        try:
            institution = self.results.get("article_info", {}).get("institution")
            if not institution:
                print("Institution name not found in the article.")
                return {}
            query = f"\"{institution}\" credibility reliability"
            search_results = self.retriever.get_retrieval_results(query, search_depth=5)
            if not search_results:
                print("No search results found.")
                return {}
            compact_search_results = "\n----\n".join([f"{i+1}. {s['title']}: {s['displayLink']}\n{s['summary']}" for i, s in enumerate(search_results)])

            client = genai.Client(api_key=self.LLM_API_KEY)
            res = client.models.generate_content(
                model=self.LLM_MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction="You are an agent proficient in journalism.",
                ),
                contents = prompt_lib["institution_survey_prompt"].format(institution=institution, search_results=compact_search_results),
            )
            res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            res["institution_search_references"] = [s["displayLink"] for s in search_results]
            self.results["institution_bias_analysis"] = res
            return res

        except Exception as e:
            print(f"Error during prior bias analysis: {e}")
            raise e


    def fact_check(self):
        # TODO:
        # Evaluate the accuracy of each alleged fact.
        # Cross-reference with credible online sources and apply logical reasoning.
        # Categorize each fact as Verified, Partly True / Misleading, False, Disputed / Inconclusive, or Unverifiable.
        # Include citations for all supporting information.
        pass


    def get_opposite_perspective(self):
        # TODO:
        # Identify opposing viewpoints for each opinion expressed in the article.
        # Search online for credible sources presenting counterarguments.
        # Summarize key points and provide citations.
        pass

    def get_bias_conclusion(self):
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

        self.article_pre_analysis()
        self.institution_bias_analysis()
        self.fact_check()
        self.get_opposite_perspective()
        self.get_bias_conclusion()

        return self.results




        