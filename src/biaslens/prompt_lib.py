prompt_lib = {

    "article_reading_prompt" : (
        "Carefully read the following article from news websites or social media, and retain all relevant information and details. "
        "Please hold on — I'll ask you questions about it shortly. Here is the article:\n"
    ),


    "article_information_extract_prompt" : (
        "Now based on the content provided above, extract and return the following information in JSON format:\n"
        "- The list of author(s) and/or commentators\n"
        "- The primary news institution responsible for the publication, if any\n"
        "- The news category (e.g., Politics, Technology, Sports)\n"
        "- The time or date of the described events (use publication time if unknown)\n"
        "- A concise abstract (1–3 sentence summary)\n"
        "- The list of main entities covered (e.g., individuals, organizations, or groups), with a maximum of 5.\n\n"
        "For any unknown or not applicable information, leave it empty (\"\" or []) as a placeholder. Respond only with a JSON object in the following format:\n"
        "{\"authors\": [\"xxx\", \"xxx\", ...], \"institution\": \"xxx\", \"category\": \"xxx\", \"time\": \"xxx\", \"abstract\": \"xxx\", \"entities\": [\"xxx\", \"xxx\", ...]}\n"
    ),


    "article_argument_extract_prompt" : (
        "Extract the key opinions and alleged facts from the article. "
        "An *opinion* is a subjective statement or suggestion made by the author/commentator that cannot be definitively classified as true or false. "
        "An *alleged fact* is a statement, assertion, or conclusion that can be verified as true or false. "
        "Include only the most important opinions and alleged facts, limiting each to a maximum of 3. Ensure each entry is concise and clearly worded. "
        "If no opinions or alleged facts are present, leave the respective lists empty.\n\n"
        "To facilitate further research:\n"
        "- For each opinion, provide a search query that could help find opposing viewpoints online.\n"
        "- For each alleged fact, provide a search query that can help verify its accuracy using online information.\n\n"
        "Format your response as a JSON object, as shown below:\n\n"
        
        "{\n"
        "  \"opinions\": [\"The US should raise tariffs\", \"The US is likely to usher in a return of manufacturing\"],\n"
        "  \"opposite_opinion_queries\": [\"tariffs bad for US economy\", \"US return of manufacturing difficulty\"],\n"
        "  \"alleged_facts\": [\"The US has a huge trade deficit\", \"Most Americans support tariffs\"],\n"
        "  \"verify_fact_queries\": [\"US trade balance\", \"Tariff poll US 2025\"]\n"
        "}\n"
    ),


    "article_tendency_extract_prompt" : (
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
        
        "- **Entities Tendency**: For the list of entities you provided earlier, indicate the article's attitude toward each:\n"
        "  1. \"Positive\"\n"
        "  2. \"Negative\"\n"
        "  3. \"Neutral\"\n"
        "  (Leave any entry as \"\" if not applicable)\n\n"
        
        "Respond only with a JSON object in the following format (e.g.):\n"
        "{\"language_style\": \"Subjective / Emotional\", \"political_tendency\": \"\", \"entities_tendency\": [\"Positive\", \"\", \"Neutral\"]}"
    )
}