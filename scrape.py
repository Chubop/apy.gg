import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, NavigableString
from bs4.element import Comment
import re
from pprint import pprint


st = ""


def remove_invisible_elements(driver, element):

    children = element.find_elements(By.XPATH, "./*")
    for child in children:
        if not child.is_displayed():
            # If the child is not displayed, remove it from the DOM
            driver.execute_script("arguments[0].remove()", child)
        else:
            # If the child is displayed, recursively process its children
            remove_invisible_elements(driver, child)


def find_strings(tag):
    global st
    if isinstance(tag, NavigableString):
        if tag.strip() and '<' not in tag:
            st += ' ' + (tag.strip())
    elif 'display: none' not in tag:
        for child in tag.children:
            find_strings(child)
    return st


def find_floats(string, regex: str = r"(?:^|(?<=\s))(\d\.\d{2})(%?)(?=\D|$)"):
    matches = re.finditer(regex, string, re.MULTILINE)
    floats = []
    for matchNum, match in enumerate(matches, start=1):
        floats.append(match)
    return floats


def clean_string(s):
    # Replace multiple newlines with a single newline
    s = re.sub(r'\n+', '\n', s)
    # Remove leading and trailing spaces and tabs
    s = s.strip()
    # Replace multiple spaces and tabs with a single space
    s = re.sub(r'[ \t]+', ' ', s)
    # Return the cleaned string
    return s


def scrape_site(url, debug=False):
    driver = webdriver.Chrome()

    # navigate to the webpage
    driver.get(url)
    root = driver.find_element(By.XPATH, "//*")
    remove_invisible_elements(driver, root)
    # get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    updated_page_source = driver.page_source
    soup = BeautifulSoup(updated_page_source, 'html.parser')
    # remove all the meta tags
    print(soup.get_text())
    for meta in soup.find_all('meta'):
        meta.decompose()
    for script in soup.find_all('script', src=False):
        script.decompose()
    # find all the header elements, spans, and divs with text as their direct children
    # print the text content of each element
    text = find_strings(soup)
    if debug is True:
        print(text)
    # Define the pattern to find the APY%
    floats = find_floats(text)
    apy_rates = []
    for match in floats:
        end_pos = match.end()
        surrounding_text = text[end_pos - 25:end_pos + 25].lower()
        if 'apy' in surrounding_text:
            # make a tuple of the percent value, and then the surrounding text. if APY% is nearby, append to list
            apy_rates.append((match.group(0), surrounding_text))

    # close the browser
    driver.quit()
    pprint(apy_rates)
    print(apy_rates[0])
    if len(apy_rates) > 1:
        import statistics
        apy_rates = [float(rate[0].strip('%')) for rate in apy_rates]
        # calculate the mode of the APY rates
        mode = statistics.mode(apy_rates)
        return mode
    else:
        return apy_rates[0][0]


if __name__ == '__main__':
    url = "https://www.tiaabank.com/banking/rates?accounts=savings"
    scrape_site(url, debug=True)
