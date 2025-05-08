import json
import google.generativeai as genai
from google.generativeai import types
from datetime import datetime

from .prompt_lib import prompt_lib
from .utils import QueryWebRetriever


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
        genai.configure(api_key=LLM_API_KEY)
        self.LLM_API_KEY = LLM_API_KEY
        self.LLM_MODEL_NAME = LLM_MODEL_NAME
        self.retriever = QueryWebRetriever(LLM_API_KEY, LLM_MODEL_NAME, SEARCH_ENGINE_ID, SEARCH_API_KEY)
        self.page_gross_text = req.get("page_gross_text")
        self.page_url = req.get("page_url")


    def article_pre_analysis(self):
        model = genai.GenerativeModel(self.LLM_MODEL_NAME)
        chat = model.start_chat(history=[])

        # read the article
        chat.send_message(
            prompt_lib["article_reading_prompt"].format(article='[' + self.page_url + '] ' + self.page_gross_text)
        )

        self.article_info = {}
        res = chat.send_message(prompt_lib["article_information_extract_prompt"])
        res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
        self.article_info = json.loads(res)

        self.article_intent = {}
        res = chat.send_message(prompt_lib["article_expressive_intent_extract_prompt"])
        res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
        self.article_intent = json.loads(res)

        
        if "opinion" in self.article_intent.get("expressive_intent").lower() or self.article_intent.get("expressive_intent") == "":
            prompt_prefix = "op"
        else:
            prompt_prefix = "news"
        
        self._article_arguments = {}
        res = chat.send_message(prompt_lib[f"{prompt_prefix}_argument_extract_prompt"])
        res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
        self._article_arguments = json.loads(res)

        self.article_tendency = {}
        res = chat.send_message(prompt_lib["article_tendency_extract_prompt"])
        res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
        self.article_tendency["entities"] = self.article_info.get("entities", [])
        self.article_tendency.update(json.loads(res))

        return self.article_info, self.article_intent, self.article_tendency

    
    def institution_bias_analysis(self):
        try:
            self.institution_bias = {}

            institution = self.article_info.get("institution")
            if not institution:
                print("Institution name not found in the article.")
                return {}
            query = f"\"{institution}\" credibility reliability"
            search_results = self.retriever.get_retrieval_results(query, search_depth=5)
            if not search_results:
                print("No search results found.")
                return {}
            compact_search_results = "\n----\n".join([f"{i+1}. {s['title']}: {s['displayLink']}\n{s['summary']}" for i, s in enumerate(search_results)])

            model = genai.GenerativeModel(self.LLM_MODEL_NAME)
            res = model.generate_content(
                prompt_lib["institution_survey_prompt"].format(institution=institution, search_results=compact_search_results)
            )
            res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
            self.institution_bias["institution"] = institution
            self.institution_bias.update(json.loads(res))
            self.institution_bias["institution_search_references"] = [s["link"] for s in search_results]
            return self.institution_bias

        except Exception as e:
            print(f"Error during prior bias analysis: {e}")
            raise e


    def fact_check(self):
        self.fact_check_res = []
        for alleged_fact, query in zip(self._article_arguments.get("alleged_facts", []), self._article_arguments.get("verify_fact_queries", [])):
            search_results = self.retriever.get_retrieval_results(query, search_depth=5)
            if not search_results:
                print(f"No search results found for query: {query}")
                continue
            compact_search_results = "\n----\n".join([f"{i+1}. {s['title']}: {s['displayLink']}\n{s['summary']}" for i, s in enumerate(search_results)])

            model = genai.GenerativeModel(self.LLM_MODEL_NAME)
            res = model.generate_content(
                prompt_lib["fact_check_prompt"].format(alleged_fact=alleged_fact, current_date=datetime.now().strftime("%B, %Y"), article_time=self.article_info["time"], search_results=compact_search_results)
            )
            res = res.text.strip().removeprefix("```json").removesuffix("```").strip()
            res = json.loads(res)
            f_r = {}
            f_r["alleged_fact"] = alleged_fact
            f_r.update(res)
            f_r["fact_check_search_references"] = [s["link"] for s in search_results]
            self.fact_check_res.append(f_r)
            
        return self.fact_check_res


    def get_opposite_perspective(self):
        if not ("opinion" in self.article_intent.get("expressive_intent").lower()):
            print("The article is not an opinion piece, so no opposite perspective is needed.")
            return []

        self.perspective_res = []
        for opinion, query in zip(self._article_arguments.get("opinions", []), self._article_arguments.get("opposite_opinion_queries", [])):
            search_results = self.retriever.get_retrieval_results(query, search_depth=5)
            if not search_results:
                print(f"No search results found for query: {query}")
                continue
            compact_search_results = "\n----\n".join([f"{i+1}. {s['title']}: {s['displayLink']}\n{s['summary']}" for i, s in enumerate(search_results)])

            model = genai.GenerativeModel(self.LLM_MODEL_NAME)
            op_opinion = model.generate_content(
                prompt_lib["opposite_search_results_summary_prompt"].format(search_results=compact_search_results)
            )
            op_opinion = op_opinion.text
            res = {}
            res["opinion"] = opinion
            res["opposite_opinion"] = op_opinion
            res["opposite_opinion_search_references"] = [s["link"] for s in search_results]
            
            self.perspective_res.append(res)
        
        return self.perspective_res


    def get_conclusion(self):
        model = genai.GenerativeModel(self.LLM_MODEL_NAME)
        if "opinion" in self.article_intent.get("expressive_intent").lower():
            prompt = prompt_lib["op_conclusion_prompt"].format(
                expressive_intent=self.article_intent.get("expressive_intent"),
                institution=self.article_info.get("institution"),
                article = self.page_gross_text,
                language_style=self.article_tendency.get("language_style"),
                alleged_facts = "\n".join([f"{i+1}. {f['alleged_fact']}: {f['fact_check']}. {f['fact_check_reason']}" for i, f in enumerate(self.fact_check_res)]),
                opinions = "\n".join([f"{i+1}. [Content Opinion]: {o['opinion']}; [Opposite Opinion]: {o['opposite_opinion']}" for i, o in enumerate(self.perspective_res)])
            )
        else:
            prompt = prompt_lib["news_conclusion_prompt"].format(
                expressive_intent=self.article_intent.get("expressive_intent"),
                institution=self.article_info.get("institution"),
                article = self.page_gross_text,
                language_style=self.article_tendency.get("language_style"),
                alleged_facts = "\n".join([f"{i+1}. {f['alleged_fact']}: {f['fact_check']}. {f['fact_check_reason']}" for i, f in enumerate(self.fact_check_res)]),
            )

        bias_conclusion = model.generate_content(prompt)
        bias_conclusion = bias_conclusion.text.strip().removeprefix("```json").removesuffix("```").strip()
        bias_conclusion = json.loads(bias_conclusion)

        return bias_conclusion

        


        


        