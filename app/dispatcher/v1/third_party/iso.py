import urllib.request
from os import path
from typing import List

from app.constants import settings
from app.dispatcher.v1.base import CurrencyDispatcher
from app.schemas import Currency
from bs4 import BeautifulSoup


class Iso(CurrencyDispatcher):
    PREFIX = settings.ISO_CRAWLER_STR
    STATIC_FILE = settings.STATIC_FILE

    def get_currencies(self) -> List[Currency]:
        currencies = []
        if not (currencies := self.get_currencies_from_static_files()):
            currencies = self.get_currencies_from_url()
        return currencies

    def get_currencies_from_url(self) -> List[Currency]:
        url_str = self.PREFIX + "/list_one.xml"
        xml_str = urllib.request.urlopen(url_str).read()
        return self.get_currencies_from_xml(xml_str)

    def get_currencies_from_static_files(self) -> List[Currency]:
        file_str = self.STATIC_FILE + "/get_currencies.xml"
        if not path.exists(file_str):
            return []

        xml_str = open(file_str, "r").read()
        return self.get_currencies_from_xml(xml_str)

    def get_currencies_from_xml(self, xml_str: str) -> List[Currency]:
        soup = BeautifulSoup(xml_str, "xml")
        nations = soup.find_all("CcyNtry")

        currencies = []
        for nation in nations:
            currency_code = nation.find("Ccy")
            currency_name = nation.find("CcyNm")
            currency_number = nation.find("CcyNbr")
            country_name = nation.find("CtryNm")

            if currency_code is None:
                continue

            currency = Currency(
                code=currency_code.string.upper(),
                name=currency_name.string.capitalize(),
                number=int(currency_number.string),
                country=country_name.string.capitalize(),
            )
            currencies.append(currency)
        return currencies

    def get_currency(self, code: str) -> Currency:
        currency = None
        if not (currency := self.get_currency_from_static_files(code)):
            currency = self.get_currency_from_url(code)
        return currency

    def get_currency_from_url(self, code: str) -> List[Currency]:
        url_str = self.PREFIX + "/list_one.xml"
        xml_str = urllib.request.urlopen(url_str).read()
        return self.get_currency_from_xml(code, xml_str)

    def get_currency_from_static_files(self, code: str) -> List[Currency]:
        file_str = self.STATIC_FILE + "get_currencies.xml"
        if not path.exists(file_str):
            return []

        xml_str = open(file_str, "r").read()
        return self.get_currency_from_xml(code, xml_str)

    def get_currency_from_xml(self, code: str, xml_str: str) -> List[Currency]:
        soup = BeautifulSoup(xml_str, "xml")
        currency_code = soup.find("Ccy", string=code.upper())
        nation = currency_code.find_parent("CcyNtry")

        currency_code = nation.find("Ccy")
        currency_name = nation.find("CcyNm")
        currency_number = nation.find("CcyNbr")
        country_name = nation.find("CtryNm")

        currency = Currency(
            code=currency_code.string.upper(),
            name=currency_name.string.capitalize(),
            number=int(currency_number.string),
            country=country_name.string.capitalize(),
        )
        return currency


iso = Iso()
