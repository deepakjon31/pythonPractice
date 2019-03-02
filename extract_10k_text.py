import requests
import re
import traceback
from requests.exceptions import ConnectionError, ConnectTimeout
from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer as ST

LXML = 'lxml'
ONLY_FONT_TAGS = 'div'
NoneType = type(None)


class ExtractText(object):
    def __init__(self):
        self.only_font_tags = ST(ONLY_FONT_TAGS)

    def _get_response(self, url):
        try:
            res = requests.get(url)
            if res.status_code == requests.codes.ok:
                return res.content
            raise ConnectionAbortedError()
        except (ConnectionError, ConnectTimeout) as e:
            print(f'Error: {e}')
            traceback.print_exc(e)
            
    def extract_10k_text(self, url):
        soup = BS(self._get_response(url), LXML, parse_only=self.only_font_tags)
        fonts = soup.find_all('font')
        previous_header = ''
        temp_text = ''
        table = []
        page = 0
        for font in fonts:
            font_style = font.get('style')
            if 'bold' in font_style:
                table.append((previous_header, temp_text, page))
                previous_header = font.getText()
                temp_text = ''
            else:
                text = font.getText()
                temp_text += text
                if re.search(r'\d{1,3}', text.strip()):
                    if len(text.strip()) < 4 and '%' not in text:
                        _page = font.parent.parent.get('style')
                        if _page is not None:
                            if 'text-align:center' in _page:
                                page = text
        import pandas as pd
        data = pd.DataFrame(table)
        data.to_csv('deepak_10k.csv', index=False)

        
if __name__ == "__main__":
    obj = ExtractText()
    obj.extract_10k_text('https://www.sec.gov/Archives/edgar/data/1018724/000101872419000004/amzn-20181231x10k.htm')
