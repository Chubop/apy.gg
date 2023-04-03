import unittest
import json
from scrape import scrape_site
from gpt import get_apy


class TestScrapingAccuracy(unittest.TestCase):
    def test_banks_json(self):
        with open('banks.json', 'r') as file:
            banks = json.load(file)
        for bank in banks['banks']:
            x, y, z = bank['name'], bank['apy_source_url'], bank['expected_rate']
            print('Testing', x)
            apys = scrape_site(y)
            apy = get_apy(apys)
            is_match = apy == z
            print('\t', end="")
            print(is_match if is_match is True else 'expected', z, ', got', apy)
            with self.subTest(msg=x):
                self.assertEqual(apy, z)

