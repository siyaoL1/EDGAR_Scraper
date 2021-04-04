import re
from typing import List
import requests
from lxml import html
import lxml

BASE_URL = "https://www.sec.gov"


def get_10k_year(url):
    url = url.split('/')
    return '20' + url[7][10:12]


def get_10Q_year_seq_number(url):
    url = url.split('/')
    return ['20' + url[7][10:12], url[7][12:]]


class Company:

    def __init__(self, name, cik, timeout=10):
        self.name = name
        self.cik = cik
        self.url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        self.timeout = timeout
        self._document_urls = []
        self._excel_urls = []
        # [url, year]
        # [url, year, quarterNumber]
        self.form_type = {'10-K': [], '10-Q': []}

    @property
    def document_urls(self):
        return list(set(self._document_urls))

    def _get(self, url):
        return requests.get(url, timeout=self.timeout)

    def get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> str:
        url = self.url + "&type=" + filing_type + "&dateb=" + prior_to + "&owner=" + ownership + "&count=" + str(
            no_of_entries)
        return url

    def get_all_filings(self, filing_type="", prior_to="", ownership="include",
                        no_of_entries=100) -> lxml.html.HtmlElement:
        url = self.get_filings_url(filing_type, prior_to, ownership, no_of_entries)
        page = self._get(url)
        return html.fromstring(page.content)

    def get_company_excel_reports_from(self, report_type) -> List[str]:
        """
        Retrieve the company's excel format 10-K or 10-Q report
        """
        # determine type of request
        regex = re.search('10-K|10-Q', report_type)
        if not regex:
            return None

        page = self.get_all_filings(filing_type=report_type)

        self._document_urls = [BASE_URL + elem.attrib["href"]
                               for elem in page.xpath("//*[@id='documentsbutton']") if elem.attrib.get("href")]

        # add to the form_type dict
        for elem in self._document_urls:
            new_url = '/'.join(elem.split('/')[:-1] + ["Financial_Report.xlsx"])
            if report_type == '10-K':
                new_url = [new_url, get_10k_year(new_url)]
            else:
                year_seq = get_10Q_year_seq_number(new_url)
                # figure out how to put them into quarters
                new_url = (new_url, year_seq[0], year_seq[1])

            self.form_type[report_type].append(new_url)

        return self._excel_urls

    def download_file(self, url, cid) -> bool:
        if not cid == self.cik:
            return False

        req = requests.get(url, allow_redirects=True)
        file = open('report_' + self.name + '.xlsx', 'wb')
        file.write(req.content)
        file.close()
        return True

    # return all 10-K and 10-Q's
    def get_form_types(self):
        return self.form_type

    # return 10-K
    def get_10k_year(self, year):
        tenK_lst = self.form_type['10-K']
        for idx in tenK_lst:
            if idx[1] == year:
                return idx[0]
        return None

    # return 10-Q
    def get_10Q_year(self, year, quarter):
        tenK_lst = self.form_type['10-K']
        for idx in tenK_lst:
            if idx[1] == year:
                if idx[2] == quarter:
                    return idx[0]
        return None

