import asyncio, json
import data_vis
from scraper import scrape_bank
from pprint import pprint
from random import shuffle


async def check_bank_scraper():
    whole = valids = 0
    failed_banks = []
    tests = [] # tests passed in for data_vis
    print("Starting test.")
    file_name = 'banks.json'
    with open(file_name, 'r') as file:
        banks = json.load(file)

    shuffle(banks)
    for bank in banks['banks']:
        name, url, expected_rate = bank['name'], bank['apy_source_url'], bank['expected_rate']
        print(f'Testing {name}...', end="")
        apy = await scrape_bank(url=url)
        is_match = apy == expected_rate
        if is_match:
            print('\t' + str(is_match))
            valids += 1
        else:
            print('\t' + str(is_match), f"Expected {expected_rate}, but got {apy}.")
            failed_banks.append( (name, url))
        whole += 1
        print('Current Accuracy:', valids, '/', whole, ',', float(valids/whole))
        tests.append(float(valids/whole) * 100)
    print("===RESULTS===")
    print(str(valids) + '/' + str(whole), "tests passed.")
    print(str(float(valids / whole)) + '%', "success rate")
    if len(failed_banks) > 0:
        print("Failed Banks: ")
        pprint(failed_banks)
    data_vis.map_scraper(tests)


if __name__ == '__main__':
    asyncio.run(check_bank_scraper())
