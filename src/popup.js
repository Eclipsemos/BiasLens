document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');

    // Flask backend URL - change this to your deployed URL in production
    const BACKEND_URL = 'http://127.0.0.1:5000';

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
                    document.getElementById('information').innerHTML = formatInformation(analysisResult);
                    document.getElementById('institution').innerHTML = formatInstitution(analysisResult.institution_bias);
                    document.getElementById('stance').innerHTML = formatStance(analysisResult.article_tendency);
                    document.getElementById('fact-check').innerHTML = formatFactCheck(analysisResult.fact_check);
                    document.getElementById('opposite-perspectives').innerHTML = formatOppositePerspectives(analysisResult.opposite_perspectives);
                    document.getElementById('conclusion').innerHTML = formatConclusion(analysisResult.conclusion);
                    
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


function formatInformation(analysisResult) {
    let html = '<div class="analysis-section">';
    
    if (analysisResult.article_info.author) {
        html += `<p><strong>Author:</strong> ${analysisResult.article_info.author || 'N/A'}</p>`;
    }
    if (analysisResult.article_info.time) {
        html += `<p><strong>Date:</strong> ${analysisResult.article_info.time || 'N/A'}</p>`;
    }
    if (analysisResult.article_intent) {
        html += `<p><strong>Content Type:</strong> ${analysisResult.article_intent.expressive_intent || 'N/A'}</p>`;
    }
    if (analysisResult.article_tendency){
        if (analysisResult.article_tendency.language_style) {
            html += `<p><strong>Language Style:</strong> ${analysisResult.article_tendency.language_style || 'N/A'}</p>`;
        }
    }
    if (analysisResult.article_info.abstract) {
        html += `<p><strong>Abstract:</strong> ${analysisResult.article_info.abstract || 'N/A'}</p>`;
    }

    html += '</div>';
    return html;
}


function formatInstitution(institutionBias) {
    if (!institutionBias) {
        return '<p>No institution found in this content.</p>';
    }

    const credibility = (institutionBias.credibility || '').toLowerCase(); // 'low' | 'medium' | 'high'


    const levelBar = `
        <span class="level-bar">
            <span class="level-segment low   ${credibility === 'low'    ? 'active' : ''}"></span>
            <span class="level-segment medium ${credibility === 'medium' ? 'active' : ''}"></span>
            <span class="level-segment high   ${credibility === 'high'   ? 'active' : ''}"></span>
        </span>
    `;

    return `
        <div class="institution-section">
            <p><strong>Institution:</strong> ${institutionBias.institution || 'N/A'}</p>
            <p><strong>Type:</strong> ${institutionBias.institution_type || 'N/A'}</p>


            <p class="credibility-row">
                <strong>Credibility:</strong>
                <span class="credibility-text">${institutionBias.credibility || 'N/A'}</span>
                ${levelBar}
            </p>

            ${institutionBias.credibility_reason
                ? `<p><strong>Reason:</strong> ${institutionBias.credibility_reason}</p>`
                : ''}

            ${Array.isArray(institutionBias.institution_search_references) && institutionBias.institution_search_references.length
                ? `<div class="references-section">
                        <h4>References:</h4>
                        <ul>
                            ${institutionBias.institution_search_references
                                .map(ref => `<li><a href="${ref}" target="_blank">${ref}</a></li>`)
                                .join('')}
                        </ul>
                   </div>`
                : ''}
        </div>
    `;
}




function formatStance(articleTendency) {
    if (!articleTendency) {
        return '<p>No stance found in this content.</p>';
    }
    let html = '<div class="stance-section">';
    if (articleTendency.entities && articleTendency.entities_tendency) {
        for (let i = 0; i < articleTendency.entities.length; i++) {
            html += `<li><strong>${articleTendency.entities[i]}</strong>: ${articleTendency.entities_tendency[i] || 'N/A'}</li>`;
        }
    html += '</div>';
    return html;
    }
}


function formatFactCheck(factChecks) {
    if (!factChecks || factChecks.length === 0) {
        return '<p>No alleged fact found in this content.</p>';
    }

    let html = '<div class="fact-check-section">';
    factChecks.forEach((fact, index) => {
        html += `<div class="fact-item">
            <h4>Fact ${index + 1}</h4>
            <p><strong>Statement:</strong> ${fact.alleged_fact}</p>
            <p><strong>Verification:</strong> ${fact.fact_check}</p>
            <p><strong>Reasoning:</strong> ${fact.fact_check_reason}</p>`;
        
        if (fact.fact_check_search_references) {
            html += '<div class="references-section">';
            html += '<h5>References:</h5><ul>';
            fact.fact_check_search_references.forEach(ref => {
                html += `<li><a href="${ref}" target="_blank">${ref}</a></li>`;
            });
            html += '</ul></div>';
        }
        
        html += '</div>';
    });
    html += '</div>';
    return html;
}


function formatOppositePerspectives(oppositePerspectives) {
    if (!oppositePerspectives || oppositePerspectives.length === 0) {
        return '<p>This content does not express any opinions explicitly.</p>';
    }

    let html = '<div class="opposite-perspectives-section">';
    oppositePerspectives.forEach((perspective, index) => {
        html += `<div class="perspective-item">
            <h4>Perspective ${index + 1}</h4>
            <p><strong>Author's Opinion:</strong> ${perspective.opinion}</p>
            <p><strong>Opposing Opinion Online</strong> ${perspective.opposite_opinion}</p>`;
        if (perspective.opposite_opinion_search_references) {
            html += '<div class="references-section">';
            html += '<h5>References:</h5><ul>';
            perspective.opposite_opinion_search_references.forEach(ref => {
                html += `<li><a href="${ref}" target="_blank">${ref}</a></li>`;
            });
            html += '</ul></div>';
        }
        html += '</div>';
    });
    html += '</div>';
    return html;

}

function formatConclusion(conclusion) {
    if (!conclusion) {
        return '<p>No conclusion generated.</p>';
    }


    const ratingRaw = (conclusion.rating || '').toLowerCase();
    let activeCount = 0;
    let colorClass  = '';

    switch (ratingRaw) {
        case 'excellent':
            activeCount = 4;  colorClass = 'excellent';  break;
        case 'good':
            activeCount = 3;  colorClass = 'good';       break;
        case 'average':
            activeCount = 2;  colorClass = 'average';    break;
        case 'poor':
            activeCount = 1;  colorClass = 'poor';       break;
        case 'unverifiable':
        default:
            activeCount = 0;  colorClass = 'unverifiable'; break;
    }

    const ratingBar = `
        <span class="rating-bar">
            ${Array.from({ length: 4 }).map((_, i) =>
                `<span class="rating-segment ${
                    i < activeCount ? `active ${colorClass}` : ''
                }"></span>`).join('')}
        </span>
    `;

    return `
        <div class="conclusion-section">
            <p class="rating-row">
                <strong>Overall Rating:</strong>
                <span class="rating-text">${conclusion.rating || 'N/A'}</span>
                ${ratingBar}
            </p>
            <p><strong>Conclusion:</strong> ${conclusion.conclusion || 'N/A'}</p>
        </div>
    `;
}
