import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scrape_bank_data():
    url = 'https://www.depositaccounts.com/savings/'  # Replace this with the target URL

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        # Click the "Show All" button
        show_all_button = page.locator('a:has-text("Show All")')
        show_all_button.click()
        time.sleep(2)
        # Get the page content after clicking the button
        content = page.content()

        soup = BeautifulSoup(content, 'html.parser')
        rate_table = soup.find('div', id='rateTable')
        entries = rate_table.find_all('div', recursive=False)

        bank_names = []
        apy_percents = []

        for entry in entries:
            bank_div = entry.find('div', class_='bank')
            if bank_div:
                bank_names.append(bank_div.text.strip().replace("Reviews",""))

            right_div = entry.find('div', class_='right')
            if right_div:
                apy_div = right_div.find('div', class_='apy')
                if apy_div:
                    apy_span = apy_div.find('span')
                    if apy_span:
                        apy_percents.append(apy_span.text.strip())

        browser.close()

    return bank_names, apy_percents


if __name__ == '__main__':
    banks, apys = scrape_bank_data()
    print('Banks:', banks)
    print('APYs:', apys)
    banks_adjusted = list(zip(banks, apys))
    sorted_list = sorted(banks_adjusted, key=lambda x: float(x[1].strip('%*†')), reverse=True)
    pprint(sorted_list)
