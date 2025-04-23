

class Article:
    # This class represents a news article and provides methods to analyze its content.

    def __init__(self, page_gross_text):
        self.page_gross_text = page_gross_text


    def setup_info(self, title="", authors=[], institution="", category="", time="", abstract="", entities=[]):
        # This method sets up the article information.
        
        self.title = title
        self.authors = authors
        self.institution = institution
        self.category = category
        self.time = time
        self.abstract = abstract
        self.entities = entities


    def setup_claims(self, claims=[], queries=[]):
        # This method sets up the article claims.
        
        self.claims = claims
        self.claim_queries = queries