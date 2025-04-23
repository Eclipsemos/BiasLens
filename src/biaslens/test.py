from biaslens import BiasLens




if __name__ == "__main__":
    # Example usage

    sample_request = {
        "page_gross_text": \
            "Musk says time commitment to DOGE will 'drop significantly' as focus returns to Tesla\nTesla reported dismal earnings and warned that politics and Trump's tariff policies would take a toll on the company. Musk said he would advocate for lower tariffs.\nApril 22, 2025, 3:34 PM CDT / Updated April 22, 2025, 5:12 PM CDT\nBy Rob Wile and David Ingram\nTech billionaire Elon Musk said Tuesday that he will begin dedicating more time to Tesla and less to his work with the Trump administration starting next month, providing a relief to Tesla investors fed up with his political work and signaling a possible shift in power at the White House.\nMusk's comments came on Tesla's call with investors following the company reporting a sizable drop in first-quarter profit and revenue. The company warned that the political environment along with the Trump administration's tariff plans were challenges for its business."
    }

    lens = BiasLens(sample_request)