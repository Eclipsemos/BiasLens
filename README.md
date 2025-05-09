# BiasLens - News Bias Analysis Chrome Extension

BiasLens is a Chrome extension that helps users analyze news articles for bias, verify facts, and explore alternative perspectives. It provides a comprehensive analysis of news content, including article intent, institutional bias, fact-checking, and opposing viewpoints.

## Architecture

```mermaid
graph TD
    A[Chrome Extension] --> B[Content Script]
    B --> C[Article Content]
    A --> D[Popup UI]
    D --> E[Analyze Button]
    E --> F[Flask Backend]
    F --> G[Article Analysis]
    G --> H[Bias Analysis]
    G --> I[Fact Check]
    G --> J[Institution Analysis]
    G --> K[Alternative Perspectives]
    H --> L[Results Display]
    I --> L
    J --> L
    K --> L
    L --> D

    subgraph Frontend
        A
        B
        D
        E
        L
    end

    subgraph Backend
        F
        G
        H
        I
        J
        K
    end
```

## Features

- **Bias Analysis**: Analyzes articles for potential bias and framing
- **Fact Checking**: Verifies key claims in the article with references
- **Institution Analysis**: Evaluates the credibility of news sources
- **Alternative Perspectives**: Provides opposing viewpoints and additional context
- **Reference Links**: Includes clickable references for all analyses

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser
- pip (Python package manager)

### Backend Setup
1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/BiasLens.git
  cd BiasLens
  ```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```


3. Configure API Keys via Environment Variables:


   1. Create a `.env` file in the `src/` directory.

   2. Add your credentials, including LLM API keys, model names, and search engine API keys and IDs.
      For example:

      ```bash
      # src/.env
      
      LLM_API_KEY = AIsiHyQjsOlX-oapsLOycq7CNjhopiw7l-BQ1RP
      LLM_MODEL_NAME = gemini-2.0-flash-lite
      
      SEARCH_API_KEY = AIioPqPLKH-20pQ17QopkoWrLHPUI98f2po8v40
      SEARCH_ENGINE_ID = 21a51tfq2167r0qr1
      ```


4. Start the Flask backend server:
```bash
python src/app.py
```

### Chrome Extension Setup
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `src` directory from the BiasLens project
4. The BiasLens extension icon should appear in your Chrome toolbar

## Usage

1. Navigate to any news article you want to analyze
2. Click the BiasLens icon in your Chrome toolbar
3. Click the "Analyze" button in the popup
4. Wait for the analysis to complete (this may take a few seconds)
5. Review the results:
   - Article Information (title, author, date)
   - Article Intent and Tendency
   - Institution Analysis with credibility rating
   - Fact Check results with references
   - Alternative perspectives (if available)

## Analysis Components

### Article Information
- Title, author, and publication date
- Abstract or summary of the article

### Article Intent
- Identifies the type of content (e.g., News, Opinion, Analysis)
- Analyzes the language style and framing

### Institution Analysis
- Evaluates the credibility of the news source
- Provides reasoning for the credibility rating
- Includes reference links for verification

### Fact Check
- Verifies key claims in the article
- Provides verification status (Verified, Partly True, Misleading)
- Includes reasoning and reference links

### Alternative Perspectives
- Presents opposing viewpoints
- Includes reference links to related articles
- Helps provide a more complete picture of the topic

## Development

### Project Structure
```
BiasLens/
├── src/
│   ├── app.py              # Flask backend server
│   ├── manifest.json       # Chrome extension manifest
│   ├── popup.html          # Extension popup interface
│   ├── popup.js            # Frontend logic
│   ├── popup.css           # Frontend styles
│   ├── content.js          # Content script for article extraction
│   ├── background.js       # Background script
│   └── config.cfg          # Configuration file
└── requirements.txt        # Python dependencies
```

### Dependencies
The project uses the following main dependencies:
- **Frontend**:
  - Chrome Extension APIs
  - HTML/CSS/JavaScript
- **Backend**:
  - Flask (Web server)
  - Flask-CORS (Cross-origin resource sharing)
  - Requests (HTTP client)
  - BeautifulSoup4 (HTML parsing)
  - Newspaper3k (Article extraction)
  - NLTK (Natural Language Processing)

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped improve BiasLens
- Special thanks to the open-source community for various tools and libraries used in this project

## Team Members

- Xinyun Ye [xinyuny3]
- Qichen Wang [qichen12]
- Yucong Chen [yucong3]
- Jiayuan Hong [jh79]
