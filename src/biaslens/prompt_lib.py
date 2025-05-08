prompt_lib = {

    "article_reading_prompt" : (
        "You are an agent proficient in journalism. Carefully read the following article from news websites or social media, and retain all relevant information and details. "
        "Please hold on — I'll ask you questions about it shortly. Here is the article:\n\n"
        "{article}"
    ),


    "article_information_extract_prompt" : (
        "Now based on the content provided above, extract and return the following information in JSON format:\n"
        "- The name of the primary news organization, website, or account responsible for the publication, if applicable. "
        "If it is not from an institution but from an individual platform/account, please fill in the individual's name.\n"
        "- The time or date of the described events (use publication time if unknown)\n"
        "- A concise abstract (1–3 sentence summary)\n"
        "- The list of main entities covered (e.g., individuals, organizations, or groups), with a maximum of 3.\n\n"
        "For any unknown or not applicable information, leave it empty (\"\" or []) as a placeholder. Respond only with a JSON object in the following schema:\n"
        "{\"institution\": \"xxx\", \"time\": \"xxx\", \"abstract\": \"xxx\", \"entities\": [\"xxx\", \"xxx\", ...]}\n"
    ),

    "article_expressive_intent_extract_prompt": (
        "Determine the **expressive intent** of the article by selecting the most accurate category from the list below:\n"
        "  1. \"Straight News / Factual Reporting\" - Objective, fact-based reporting with no opinion or analysis.\n"
        "  2. \"Opinion Content\" - Subjective writing that includes personal views, arguments, or evaluations.\n"
        "  3. \"Interpretive Reporting\" - Factual reporting that includes context, background, or analysis to explain significance.\n"
        "  (If none of the above apply, leave the field empty: \"\")\n\n"
        
        "Return only a JSON object in the following format (e.g.):\n"
        "{\"expressive_intent\": \"Straight News / Factual Reporting\"}"
    ),


    "news_argument_extract_prompt" : (
        "Extract the key alleged facts from the article. "
        "An *alleged fact* is a statement, assertion, or conclusion that can be verified as true or false. "
        "Include only the most important alleged facts, with a maximum of 3. Make them concise and clearly worded. "
        "To facilitate further research, "
        "for each alleged fact, provide a google search query that can help verify its accuracy using online information.\n"
        "Format your response as a JSON object, as shown below:\n\n"
        
        "{\n"
        "  \"alleged_facts\": [\"The US has a huge trade deficit\", \"Most Americans support tariffs\"],\n"
        "  \"verify_fact_queries\": [\"US trade balance\", \"Tariff poll US 2025\"]\n"
        "}\n"
    ),


    "op_argument_extract_prompt" : (
        "Extract the key opinions and alleged facts from the article. "
        "An *opinion* is a subjective statement or suggestion made by the author/commentator that cannot be definitively classified as true or false. "
        "An *alleged fact* is a statement, assertion, or conclusion that can be verified as true or false. "
        "Include only the most important opinions and alleged facts, limiting each to a maximum of 3. Ensure each entry is concise and clearly worded. "
        "If no opinions or alleged facts are present, leave the respective lists empty.\n\n"
        "To facilitate further research:\n"
        "- For each opinion, provide a google search query that could help find opposing viewpoints online.\n"
        "- For each alleged fact, provide a google search query that can help verify its accuracy using online information.\n\n"
        "Format your response as a JSON object, as shown below:\n\n"
        
        "{\n"
        "  \"opinions\": [\"The US should raise tariffs\", \"The US is likely to usher in a return of manufacturing\"],\n"
        "  \"opposite_opinion_queries\": [\"tariffs bad for US economy\", \"US return of manufacturing difficulty\"],\n"
        "  \"alleged_facts\": [\"The US has a huge trade deficit\", \"Most Americans support tariffs\"],\n"
        "  \"verify_fact_queries\": [\"US trade balance\", \"Tariff poll US 2025\"]\n"
        "}\n"
    ),


    "article_tendency_extract_prompt" : (
        "Let's now take a deeper look at the content's possible tendencies. "
        "Please analyze the content and respond by selecting from the following options:\n\n"

        "- **Language Style**: Choose the most appropriate style from the list below:\n"
        "  1. \"Descriptive / Neutral\"\n"
        "  2. \"Subjective / Emotional\"\n"
        "  3. \"Ironic\"\n"
        "  4. \"Framing / Guiding\"\n"
        "  5. \"Symbolic / Slogan-like\"\n\n"
        
        "- **Entities Tendency**: For the list of entities you provided earlier, indicate the article's presetting attitude toward each:\n"
        "  1. \"Positive\"\n"
        "  2. \"Negative\"\n"
        "  3. \"Neutral or No Presetting Tendency\"\n"
        
        "Respond only with a JSON object in the following format (e.g.):\n"
        "{\"language_style\": \"Subjective / Emotional\", \"entities_tendency\": [\"Positive\", \"Neutral or No Presetting Tendency\"]}"
    ),


    "search_summary_prompt" : (
                "Summarize the following web content related to '{query}' "
                "in {max_summary_length} words or fewer. Retain key information, data, and statistics while keeping the summary concise.\n"
                "Please only give the summary and nothing else. Here is the raw content:\n"
                "{content}\n"
    ),


    "institution_survey_prompt" : (
        "I will provide search results from Google. Please review the information and assess the **Type** and **Credibility Rating** of \"{institution}\" using the following categories:\n\n"
    
        "- **Type**:\n"
        "  1. \"Commercial\"\n"
        "  2. \"Government Affiliated\"\n"
        "  3. \"Independent\"\n"
        "  4. \"Citizen Journalism / KOL\"\n"
        "  5. \"Other\"\n\n"
        
        "- **Credibility Rating**:\n"
        "  1. \"High\"\n"
        "  2. \"Medium\"\n"
        "  3. \"Low\"\n"
        "  4. \"Unverifiable\"\n\n"

        "Please also provide a brief explanation (maximum 3 sentences) justifying your credibility rating.\n\n"

        "Respond **only** with a JSON object in the following format. Example:\n"
        "{{\"institution_type\": \"Commercial\", \"credibility\": \"High\", \"credibility_reason\": \"The NOTBBC has high credibility due to strict editorial standards, independent regulation by Ofcom, and a strong track record of balanced, fact-checked reporting.\"}}\n\n"
        
        "Here are the search results:\n{search_results}"
    ),


    "fact_check_prompt" : (
        "I will provide search results from Google. Please review the information and assess the **Fact Check** of \"{alleged_fact}\" using the following categories:\n\n"
    
        "- **Fact Check**:\n"
        "  1. \"Verified\"\n"
        "  2. \"Partly True / Misleading\"\n"
        "  3. \"False\"\n"
        "  4. \"Disputed / Inconclusive\"\n"
        "  5. \"Unverifiable\"\n\n"

        "Please also provide a very concise explanation (1 sentence) justifying your fact check.\n\n"

        "Respond **only** with a JSON object in the following format. Example:\n"
        "{{\"fact_check\": \"Verified\", \"fact_check_reason\": \"The US has a trade deficit with China, as confirmed by multiple sources.\"}}\n\n"
        
        "Here are the search results:\n{search_results}"
    ),


    "opposite_search_results_summary_prompt" : (
        "Based on the following opinion sources from Google search, provide a clear, concise opinion summarizing the content in one sentence. "
        "If multiple opinions are present in the sources, choose only the most representative. "
        "Respond with the opinion only and nothing else. Here are the source contents:\n{search_results}\n\n"
    ),


    "op_conclusion_prompt" : (
        "I will provide you with an {expressive_intent} from {institution} along with a report summarizing its journalistic analysis. "
        "Your task is to assess the overall quality of the content.\n\n"

        "First, read the article:\n"
        "{article}\n\n"

        "Here is the analysis of the content:\n"

        "1. Language style of the content: {language_style}\n\n"

        "2. Alleged facts and their fact-checks:\n"
        "{alleged_facts}\n\n"

        "3. Opinions expressed in the content and corresponding opposing views from online sources:\n"
        "{opinions}\n"

        "Based on the above information, provide a conclusion evaluating the quality of the content in 2-3 sentences. "
        "Your evaluation should consider the following dimensions:\n"
        "- Accuracy of facts\n"
        "- Adequacy of supporting evidence\n"
        "- Logical coherence of arguments\n"
        "- Overall integrity and fairness of the information presented\n\n"

        "Then, assign a quality rating using the following options:\n"
        "  1. \"Excellent\" — High-quality content with accurate facts, robust evidence, and logical coherence.\n"
        "  2. \"Good\" — Generally good quality with minor issues.\n"
        "  3. \"Average\" — Average quality with some significant issues.\n"
        "  4. \"Poor\" — Low quality with major issues.\n"
        "  5. \"Unverifiable\" — Cannot be assessed due to insufficient information.\n\n"

        "Respond **only** with a JSON object in the following format:\n"
        "{{"
        "\"conclusion\": \"[Your 3-4 sentence summary]\", "
        "\"rating\": \"[Your selected rating]\""
        "}}\n\n"

        "Do not include any additional information or explanations beyond the JSON object.\n"
    ),



    "news_conclusion_prompt" : (
        "I will provide you with an {expressive_intent} from {institution} along with a report summarizing its journalistic analysis. "
        "Your task is to assess the overall quality of the content.\n\n"

        "First, read the article:\n"
        "{article}\n\n"

        "Here is the analysis of the content:\n"

        "1. Language style of the content: {language_style}\n\n"

        "2. Alleged facts and their fact-checks:\n"
        "{alleged_facts}\n\n"

        "Based on the above information, provide a conclusion evaluating the quality of the content in 2-3 sentences. "
        "Your evaluation should consider the following dimensions:\n"
        "- Factual accuracy\n"
        "- Presence of guiding or selective framing\n"
        "- Neutrality of language\n"
        "- Overall integrity and balance of the information presented\n\n"

        "Then, assign a quality rating using the following options:\n"
        "  1. \"Excellent\" — High-quality content with accurate facts, robust evidence, and it presents information comprehensively.\n"
        "  2. \"Good\" — Generally good quality with minor issues.\n"
        "  3. \"Average\" — Average quality with some significant issues.\n"
        "  4. \"Poor\" — Low quality with major issues.\n"
        "  5. \"Unverifiable\" — Cannot be assessed due to insufficient information.\n\n"

        "Respond **only** with a JSON object in the following format:\n"
        "{{"
        "\"conclusion\": \"[Your 3-4 sentence summary]\", "
        "\"rating\": \"[Your selected rating]\""
        "}}\n\n"

        "Do not include any additional information or explanations beyond the JSON object.\n"
    )


}