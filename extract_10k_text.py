import requests
import re
import traceback
from requests.exceptions import ConnectionError, ConnectTimeout
from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer as ST

LXML = 'lxml'
ONLY_FONT_TAGS = 'div'
NoneType = type(None)
DIGITS = [i for i in range(0, 101)]
print(DIGITS)


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

    def _filter(self, text):
        text_len = len(text.strip())
        if isinstance(text, NoneType):
            return False, 0
        elif text_len < 3:
            return False, text_len
        elif 'None' in text:
            return False, 0
        elif text_len < 21:
            return True, text_len
        elif text_len > 20:
            return True, text_len

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

        # divs = soup.find_all('div')
        # previous_header = ''
        # temp_text = ''
        # table = []
        # for div in divs:
        #     text = div.getText(strip=' ')
        #     if text is None or len(text.strip()) == 0: continue
        #
        #     filter_text, text_len = self._filter(text)
        #     if filter_text:
        #         text = text.strip()
        #         if text_len < 21:
        #             print(temp_text)
        #             table.append((previous_header, temp_text))
        #             previous_header = text
        #             temp_text = ''
        #             print(previous_header, '******************************')
        #         # elif text_len > 20 and previous_header == text:
        #         #     temp_text = temp_text + ' ' + text
        #
        #         # print(previous_header, '\n', temp_text)
        #         else:
        #             print('------------------\n')
        #             print(len(text.strip()), text)
        #             temp_text = temp_text + ' ' + text
        # import pandas as pd
        # data = pd.DataFrame(table)
        # data.to_csv('deepak_10k.csv', index=False)




if __name__ == "__main__":
    obj = ExtractText()
    obj.extract_10k_text('https://www.sec.gov/Archives/edgar/data/1018724/000101872419000004/amzn-20181231x10k.htm')
