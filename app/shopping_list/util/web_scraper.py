import requests

class WebScraper:

    def __init__(self):
        pass

    def get_text_from_url(self, url: str) -> str:
        response = requests.get(url)
        html_text = response.text
        return html_text