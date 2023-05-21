import unittest
import re


class TestRegex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = """
        Jooble — is a Ukrainian IT company that operates in 71 countries. The company’s product is a job searchwebsite
        with more than 90M monthly users. According to SimilarWeb, Jooble is the second most visited employment website
        in the world, and it is among 500 top visited websites globally. Jooble is a remote-first company.
        We believe that talented people can create cool projects no matter where they are. The company’s
        headquarters are located in Kyiv. Offices in Kyiv, Uzhgorod and Lutsk are available for employees to visit
        at any time they want. Currently, 590 professionals in our team communicate in 25 different languages.
        Here are some exciting resources where you can find out more about our company: Jooble’s history 
        https://ain.ua/ — https://ain.ua/2019/03/25/fotoreportazh-jooble/ Our workspace — an episode of "DOU-revisor"
        (inspector) about the Jooble office in Kyiv — 
        https://dou.ua/lenta/articles/dou-revisor-jooble-2/. About career path possibilities in our company 
        https://hiring.jooble.org/ In case you have additional questions — there is a chatbot on this website 
        https://hiring.jooble.org/. We also have a Telegram bot for those who prefer to use their phones — 
        @jooblecandidate_bot. And also a bot for Viber — @jooblecandidate_bot. Corporate email of our Talent 
        manager — yulyia.lysnianskaia@jooble.com."""

    def regex_function(self, pattern) -> list:
        return re.findall(pattern, self.text)

    def test_part_one_extract_urls_one(self):
        expected_result = [
            'https://ain.ua/',
            'https://ain.ua/2019/03/25/fotoreportazh-jooble/',
            'https://dou.ua/lenta/articles/dou-revisor-jooble-2/.',
            'https://hiring.jooble.org/',
            'https://hiring.jooble.org/.'
        ]
        self.assertEqual(expected_result, self.regex_function(r'https?://[^\s<>"]+|www\.[^\s<>"]+'))

    def test_part_two_extract_emails(self):
        expected_result = ['yulyia.lysnianskaia@jooble.com']
        self.assertEqual(expected_result, self.regex_function(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'))

    def test_part_three_extract_telegram_viber_names(self):
        expected_result = ['@jooblecandidate_bot', '@jooblecandidate_bot']
        self.assertEqual(expected_result, self.regex_function(r'(@[a-zA-Z0-9_]+_bot)'))

    def test_part_four_extract_text_inside_parentheses(self):
        expected_result = ['inspector']
        self.assertEqual(expected_result, self.regex_function(r'\((.*?)\)'))
