from typing import Tuple, List, Any, Dict
from edgar.company import Company
from lxml import html
from tqdm import tqdm
import requests
from fuzzywuzzy import process, fuzz


class Edgar:

    def __init__(self):
        all_companies_page = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt")
        all_companies_content = all_companies_page.content.decode("latin1")
        all_companies_array = all_companies_content.split("\n")
        del all_companies_array[-1]
        all_companies_array_rev = []
        for i, item in enumerate(all_companies_array):
            if item == "":
                continue
            _name, _cik = Edgar.split_raw_string_to_cik_name(item)
            all_companies_array[i] = (_name, _cik)
            all_companies_array_rev.append((_cik, _name))
        self.all_companies_dict = dict(all_companies_array)
        self.all_companies_dict_rev = dict(all_companies_array_rev)

    def get_cik_by_company_name(self, name) -> str:
        return self.all_companies_dict[name]

    def match_company_by_company_name(self, name, top=5) -> List[Dict[str, Any]]:
        result = []
        for company, cik in tqdm(self.all_companies_dict.items()):
            result.append({"company_name": company, "cik": cik, "score": fuzz.partial_ratio(name, company)})
        return sorted(result, key=lambda row: row["score"], reverse=True)[:top]

    def get_company_name_by_cik(self, cik) -> str:
        return self.all_companies_dict_rev[cik]

    def find_company_name(self, words) -> List[str]:
        possible_companies = []
        words = words.lower()
        for company in self.all_companies_dict:
            if all(word in company.lower() for word in words.split(" ")):
                possible_companies.append(company)
        return possible_companies

    @classmethod
    def split_raw_string_to_cik_name(cls, item):
        item_arr = item.split(":")[:-1]
        return ":".join(item_arr[:-1]), item_arr[-1]
