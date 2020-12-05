import requests
from bs4 import BeautifulSoup

class Website:

    def __init__(self, url):
        headers = {}

        self.response = requests.get(url, timeout=5, headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        })
        soup         = BeautifulSoup(self.response.text, 'html.parser')
        body_content = soup.find('body')
        body_script = body_content.findAll('script')
        for script in body_script:
            script.extract()
        self.result  = ' '.join(body_content.findAll(text=True))
