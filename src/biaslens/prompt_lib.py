prompt_lib = {

    "article_reading_prompt" : (
        "You are an agent proficient in journalism. Carefully read the following article from news websites or social media, and retain all relevant information and details. "
        "Please hold on — I'll ask you questions about it shortly. Here is the article:\n\n"
        "{article}"
    ),


    "article_information_extract_prompt" : (
        "Now based on the content provided above, extract and return the following information in JSON format:\n"
        "- The name of the primary news organization, website, or account responsible for the publication, if applicable."
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


    "news_tendency_extract_prompt" : (
        "Let's now take a deeper look at the article's possible tendencies. "
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


    "op_tendency_extract_prompt" : (
        "Let's now take a deeper look at the article's possible tendencies. "
        "Please analyze the content and respond by selecting from the following options:\n\n"

        "- **Language Style**: Choose the most appropriate style from the list below:\n"
        "  1. \"Descriptive / Neutral\"\n"
        "  2. \"Subjective / Emotional\"\n"
        "  3. \"Ironic\"\n"
        "  4. \"Framing / Guiding\"\n"
        "  5. \"Symbolic / Slogan-like\"\n\n"
        
        "- **Political Tendency**: Select the political leaning of the article:\n"
        "  1. \"Right-wing\"\n"
        "  2. \"Center-right\"\n"
        "  3. \"Center / Not obvious\"\n"
        "  4. \"Center-left\"\n"
        "  5. \"Left\"\n"
        "  (Leave this field empty: \"\" if the article is non-political or not applicable)\n\n"
        
        "- **Entities Tendency**: For the list of entities you provided earlier, indicate the article's presetting attitude toward each:\n"
        "  1. \"Positive\"\n"
        "  2. \"Negative\"\n"
        "  3. \"Neutral or No Presetting Tendency\"\n"
        
        "Respond only with a JSON object in the following format (e.g.):\n"
        "{\"language_style\": \"Subjective / Emotional\", \"political_tendency\": \"\", \"entities_tendency\": [\"Positive\", \"Neutral or No Presetting Tendency\"]}"
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
    )
}