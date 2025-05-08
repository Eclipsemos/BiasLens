document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');

    // Flask backend URL - change this to your deployed URL in production
    const BACKEND_URL = 'http://localhost:5000';

    analyzeBtn.addEventListener('click', async function() {
        // Show loading state
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');

        try {
            // Get the active tab
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            
            // Check if we're on a valid page
            if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('edge://')) {
                throw new Error('Cannot analyze this page');
            }

            // Check if content script is available
            try {
                // Send message to content script to extract article content
                const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractContent' });
                
                if (response && response.content) {
                    // Send content to Flask backend for analysis
                    const analysisResponse = await fetch(`${BACKEND_URL}/analyze`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(response.content)
                    });

                    if (!analysisResponse.ok) {
                        throw new Error('Failed to analyze article');
                    }

                    const analysisResult = await analysisResponse.json();

                    // Display the analysis results
                    const biasAnalysis = analysisResult.bias_analysis;
                    document.getElementById('bias-analysis').innerHTML = formatBiasAnalysis(biasAnalysis);
                    document.getElementById('fact-check').innerHTML = formatFactCheck(analysisResult.fact_check);
                    
                    // Display opposite perspectives
                    displayOppositePerspectives(analysisResult.opposite_perspectives);
                    
                    // Show results
                    loadingDiv.classList.add('hidden');
                    resultsDiv.classList.remove('hidden');
                    resultsDiv.classList.remove('fade-in'); 
                    void resultsDiv.offsetWidth; 
                    resultsDiv.classList.add('fade-in');
                } else {
                    throw new Error('No content extracted');
                }
            } catch (error) {
                if (error.message.includes('Receiving end does not exist')) {
                    throw new Error('Please refresh the page and try again');
                }
                throw error;
            }
        } catch (error) {
            console.error('Error:', error);
            loadingDiv.classList.add('hidden');
            errorDiv.classList.remove('hidden');
            errorDiv.querySelector('p').textContent = error.message;
        }
    });
});

function formatBiasAnalysis(biasAnalysis) {
    let html = '<div class="analysis-section">';
    
    // Article Info
    if (biasAnalysis.article_info) {
        html += '<h3>Article Information</h3>';
        html += `<p><strong>Title:</strong> ${biasAnalysis.article_info.title || biasAnalysis.article_info.abstract || 'N/A'}</p>`;
        html += `<p><strong>Author:</strong> ${biasAnalysis.article_info.author || 'N/A'}</p>`;
        html += `<p><strong>Date:</strong> ${biasAnalysis.article_info.time || biasAnalysis.article_info.date || 'N/A'}</p>`;
    }

    // Article Intent
    if (biasAnalysis.article_intent) {
        html += '<h3>Article Intent</h3>';
        html += `<p><strong>Type:</strong> ${biasAnalysis.article_intent.expressive_intent || 'N/A'}</p>`;
    }

    // Institution Bias
    if (biasAnalysis.institution_bias) {
        html += '<h3>Institution Analysis</h3>';
        html += `<p><strong>Institution:</strong> ${biasAnalysis.institution_bias.institution || 'N/A'}</p>`;
        html += `<p><strong>Credibility:</strong> ${biasAnalysis.institution_bias.credibility || 'N/A'}</p>`;
        if (biasAnalysis.institution_bias.credibility_reason) {
            html += `<p><strong>Reason:</strong> ${biasAnalysis.institution_bias.credibility_reason}</p>`;
        }
    }

    // Conclusion
    if (biasAnalysis.conclusion) {
        html += '<h3>Overall Analysis</h3>';
        html += `<p><strong>Rating:</strong> ${biasAnalysis.conclusion.rating || 'N/A'}</p>`;
        html += `<p>${biasAnalysis.conclusion.conclusion || 'N/A'}</p>`;
    }

    html += '</div>';
    return html;
}

function formatFactCheck(factChecks) {
    if (!factChecks || factChecks.length === 0) {
        return '<p>No facts to check in this article.</p>';
    }

    let html = '<div class="fact-check-section">';
    factChecks.forEach((fact, index) => {
        html += `<div class="fact-item">
            <h4>Fact ${index + 1}</h4>
            <p><strong>Statement:</strong> ${fact.alleged_fact}</p>
            <p><strong>Verification:</strong> ${fact.fact_check}</p>
            <p><strong>Reasoning:</strong> ${fact.fact_check_reason}</p>
        </div>`;
    });
    html += '</div>';
    return html;
}

function displayOppositePerspectives(perspectives) {
    const container = document.querySelector('.perspective-links');
    container.innerHTML = ''; // Clear previous results

    if (!perspectives || perspectives.length === 0) {
        container.innerHTML = '<p>No opposing perspectives found for this article.</p>';
        return;
    }

    perspectives.forEach(perspective => {
        const perspectiveDiv = document.createElement('div');
        perspectiveDiv.className = 'perspective-item';
        
        const titleLink = document.createElement('a');
        titleLink.href = perspective.url;
        titleLink.target = '_blank';
        titleLink.textContent = perspective.title;
        
        const summary = document.createElement('p');
        summary.textContent = perspective.summary;
        
        perspectiveDiv.appendChild(titleLink);
        perspectiveDiv.appendChild(summary);
        container.appendChild(perspectiveDiv);
    });
} 