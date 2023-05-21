from bs4 import BeautifulSoup
from pathlib import Path
from lxml import etree, html
import unittest


class TestXpath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        directory = Path(__file__).resolve()
        djinni_pages_path = directory.parent / "pages_for_test"
        first_page = open(djinni_pages_path / "djinni_first_page.html", encoding='utf-8')
        cls.first_page = etree.HTML(str(BeautifulSoup(first_page, "html.parser")))

        middle_page = open(djinni_pages_path / "djinni_middle_page.html", encoding='utf-8')
        cls.middle_page = etree.HTML(str(BeautifulSoup(middle_page, "html.parser")))

        last_page = open(djinni_pages_path / "djinni_last_page.html", encoding='utf-8')
        cls.last_page = etree.HTML(str(BeautifulSoup(last_page, "html.parser")))

        html_page = open(djinni_pages_path / "xpath_part_one_xml_for_testing.html", encoding='utf-8').read()
        cls.incoming_data_for_tests = html.fromstring(bytes(html_page, encoding='utf8'))

    def xpath_part_one_first_func(self, xpath_value: str) -> list:
        res = self.incoming_data_for_tests.xpath(xpath_value)
        return [x.text for x in res]

    def xpath_part_one_second_func(self, xpath_value: str) -> str:
        return self.incoming_data_for_tests.xpath(xpath_value)[0].text

    def extract_next_page_with_xpath(self, xpath_value: str) -> tuple:
        first_page_res = self.first_page.xpath(xpath_value)
        middle_page_res = self.middle_page.xpath(xpath_value)
        last_page_res = self.last_page.xpath(xpath_value)
        return first_page_res, middle_page_res, last_page_res

    def test_extract_all_li(self):
        result = self.xpath_part_one_first_func('//ul/li')

        expected_first_element = 'Пише скрипти для парсінгу сторінок сайті;'
        expected_last_element = 'Корпоративна бібліотека з можливістю безлімітного замовлення книг.'

        self.assertEqual(expected_first_element, result[0])
        self.assertEqual(expected_last_element, result[-1])

    def test_extract_links_with_text(self):
        expected_result = "https://jobs.dou.ua/companies/jooble"
        self.assertEqual(expected_result, self.xpath_part_one_second_func("//a[contains(text(), 'https://jobs.dou.ua/')]"))

    def test_first_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], ['#'])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//li[@class="page-item active"]//following-sibling::li[1]/a[@class="page-link"]/@href'))

    def test_second_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], [])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//a[@class="btn btn-lg btn-primary"]/@href'))

    def test_third_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], ['#'])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//span[@class="sr-only"]/../../following-sibling::li[1]/a[@class="page-link"]/@href'))

    def test_fourth_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], ['#'])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//span[text()="(current)"]/../../following-sibling::li[1]/a[@class="page-link"]/@href'))

    def test_fifth_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], ['#'])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//span[@class="page-link"][descendant::span]/../following-sibling::li[1]/a[@class="page-link"]/@href'))

    def test_sixth_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], ['#'])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//span[@class="bi bi-chevron-right page-item--icon"]/../@href'))

    def test_seventh_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], ['#'])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//span[contains(@class, "bi bi-chevron-right page-item--icon") and not (@href="#")]/../@href'))

    def test_eighth_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], [])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//div[@class="d-md-none mb-3 text-center"]/a/@href'))

    def test_ninth_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], [])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//a[@class="btn btn-lg btn-primary"]/@href'))

    def test_tenth_case(self):
        expected_result = (['?page=2'], ['?page=333&page=334'], [])
        self.assertEqual(expected_result, self.extract_next_page_with_xpath('//a[contains(text(), " наступна →")]/@href'))
