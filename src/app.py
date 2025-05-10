import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from biaslens.biaslens import BiasLens
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for the Chrome extension

load_dotenv() # Load environment variables from .env file

# Initialize the analyzer with your API keys from environment variables
analyzer = BiasLens(
    req={},  # Empty dict as initial request
    LLM_API_KEY=os.getenv('LLM_API_KEY'),
    LLM_MODEL_NAME=os.getenv('LLM_MODEL_NAME'),
    SEARCH_ENGINE_ID=os.getenv('SEARCH_ENGINE_ID'),
    SEARCH_API_KEY=os.getenv('SEARCH_API_KEY')
)

@app.route('/analyze', methods=['POST'])
def analyze_article():
    try:
        article_data = request.json
        
        # Update the analyzer with new article data
        analyzer.page_gross_text = article_data.get('content', '')
        analyzer.page_url = article_data.get('url', '')
        
        # Perform the analysis
        article_info, article_intent, article_tendency = analyzer.article_pre_analysis()
        institution_bias = analyzer.institution_bias_analysis()
        fact_check_results = analyzer.fact_check()
        opposite_perspectives = analyzer.get_opposite_perspective()
        conclusion = analyzer.get_conclusion()
        
        analysis_result = {
            'bias_analysis': {
                'article_info': article_info,
                'article_intent': article_intent,
                'article_tendency': article_tendency,
                'institution_bias': institution_bias,
                'conclusion': conclusion
            },
            'fact_check': fact_check_results,
            'opposite_perspectives': opposite_perspectives
        }
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 