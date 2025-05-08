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
    // Common date selectors with more specific ones for CNN and WaPo
    const dateSelectors = [
        'time',
        '.date',
        '.published',
        '[itemprop="datePublished"]',
        'meta[property="article:published_time"]',
        '.timestamp',
        '.article__timestamp',
        '.cnn-timestamp',
        'meta[name="pubdate"]',
        'meta[name="publishdate"]',
        'meta[name="date"]',
        // CNN specific selectors
        '.update-time',
        '.update-time__text',
        '.article__timestamp',
        '.timestamp__text',
        // WaPo specific selectors
        '.display-date',
        '.article-date',
        '.timestamp__text',
        'meta[name="article:published_time"]',
        'meta[name="og:updated_time"]'
    ];

    // First try to get date from meta tags
    for (const selector of dateSelectors) {
        const element = document.querySelector(selector);
        if (element) {
            // Try to get datetime attribute first
            const datetime = element.getAttribute('datetime');
            if (datetime) {
                return datetime;
            }
            
            // Try to get content attribute for meta tags
            const content = element.getAttribute('content');
            if (content) {
                return content;
            }
            
            // Fall back to text content
            const text = element.textContent.trim();
            if (text) {
                // Try to parse CNN's date format: "Updated 10:59 AM EDT, Thu May 8, 2025"
                const cnnDateMatch = text.match(/Updated\s+.*?,\s+(.*?)\s+(\d{1,2}),\s+(\d{4})/);
                if (cnnDateMatch) {
                    const [_, month, day, year] = cnnDateMatch;
                    const monthMap = {
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                    };
                    const monthNum = monthMap[month.substring(0, 3)];
                    return `${year}-${monthNum}-${day.padStart(2, '0')}`;
                }

                // Try to parse WaPo's relative time format: "Updated 26 minutes ago"
                const wapoRelativeMatch = text.match(/Updated\s+(\d+)\s+(minute|hour|day)s?\s+ago/);
                if (wapoRelativeMatch) {
                    const [_, amount, unit] = wapoRelativeMatch;
                    const now = new Date();
                    if (unit === 'minute') {
                        now.setMinutes(now.getMinutes() - parseInt(amount));
                    } else if (unit === 'hour') {
                        now.setHours(now.getHours() - parseInt(amount));
                    } else if (unit === 'day') {
                        now.setDate(now.getDate() - parseInt(amount));
                    }
                    return now.toISOString().split('T')[0];
                }

                // Try to parse WaPo's date format: "May 8, 2025 at 10:59 AM EDT"
                const wapoDateMatch = text.match(/([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})/);
                if (wapoDateMatch) {
                    const [_, month, day, year] = wapoDateMatch;
                    const monthMap = {
                        'January': '01', 'February': '02', 'March': '03', 'April': '04',
                        'May': '05', 'June': '06', 'July': '07', 'August': '08',
                        'September': '09', 'October': '10', 'November': '11', 'December': '12'
                    };
                    const monthNum = monthMap[month];
                    return `${year}-${monthNum}-${day.padStart(2, '0')}`;
                }

                return text;
            }
        }
    }

    // Try to extract date from URL if it contains a date pattern
    const url = window.location.href;
    const datePattern = /\/(\d{4})\/(\d{2})\/(\d{2})\//;
    const match = url.match(datePattern);
    if (match) {
        const [_, year, month, day] = match;
        return `${year}-${month}-${day}`;
    }

    return null;
} 