// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'extractContent') {
        const content = extractArticleContent();
        sendResponse({ content });
    }
    return true;
});

function extractArticleContent() {
    // Common article selectors for news websites
    const selectors = [
        'article',
        '[role="article"]',
        '.article',
        '.post-content',
        '.entry-content',
        'main',
        '#main-content'
    ];

    // Try to find the main article content
    let articleElement = null;
    for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
            // Find the element with the most text content
            articleElement = Array.from(elements).reduce((a, b) => 
                a.textContent.length > b.textContent.length ? a : b
            );
            break;
        }
    }

    if (!articleElement) {
        return null;
    }

    // Extract relevant information
    const articleData = {
        title: document.title,
        url: window.location.href,
        content: articleElement.textContent.trim(),
        author: extractAuthor(),
        date: extractDate(),
        source: window.location.hostname
    };

    return articleData;
}

function extractAuthor() {
    // Common author selectors
    const authorSelectors = [
        '[rel="author"]',
        '.author',
        '.byline',
        '[itemprop="author"]',
        'meta[name="author"]'
    ];

    for (const selector of authorSelectors) {
        const element = document.querySelector(selector);
        if (element) {
            return element.textContent.trim();
        }
    }
    return null;
}

function extractDate() {
    // Common date selectors
    const dateSelectors = [
        'time',
        '.date',
        '.published',
        '[itemprop="datePublished"]',
        'meta[property="article:published_time"]'
    ];

    for (const selector of dateSelectors) {
        const element = document.querySelector(selector);
        if (element) {
            return element.getAttribute('datetime') || element.textContent.trim();
        }
    }
    return null;
} 