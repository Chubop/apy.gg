import asyncio, json, io
from contextlib import redirect_stdout
from selector_scrape import scrape_bank
from pprint import pprint


async def check_bank_scraper():
    whole = valids = 0
    failed_banks = []
    print("Starting test.")
    file_name = 'banks.json'
    with open(file_name, 'r') as file:
        banks = json.load(file)

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
    print("===RESULTS===")
    print(str(valids) + '/' + str(whole), "tests passed.")
    if len(failed_banks) > 0:
        print("Failed Banks: ")
        pprint(failed_banks)


if __name__ == '__main__':
    asyncio.run(check_bank_scraper())
