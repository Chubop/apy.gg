import unittest
import json
from scrape import scrape_site


class TestScrapingAccuracy(unittest.TestCase):
    def test_banks_json(self):
        with open('banks.json', 'r') as file:
            banks = json.load(file)
        for bank in banks['banks']:
            print('Testing', bank['name'])
            apy = scrape_site(bank['apy_source_url'])
            is_match = apy == bank['expected_rate']
            print('\t', end="")
            print(is_match if is_match is True else 'expected', bank['expected_rate'], ', got', apy)
            self.assertEqual(apy, bank['expected_rate'])
