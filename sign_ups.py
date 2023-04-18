import asyncio, time
import json
from enum import Enum
from playwright.async_api import async_playwright
from us_state_abbreviations import convert_tag


class SignUp:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class User:
    def __init__(self, user):
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.ssn = user['ssn']
        self.date_of_birth = user['date_of_birth']
        self.uses_paper = user['uses_paper']
        self.different_mailing_address = user['different_mailing_address']
        self.contact_info = user['contact_info']
        self.mailing_info = user['mailing_info']
        self.government_issued_id = user['government_issued_id']
        self.proof_of_address = user['proof_of_address']
        self.employment_info = user['employment_info']
        self.tax_info = user['tax_info']


async def capital_one_signup(info):
    bank = SignUp("Capital One", "https://apply.capitalone.com/index.html#/getting-started?productId=3800")
    user = User(info)
    print("Are you a current Capital One Customer?")
    start_input = int(input(
        "1: Yes\n2: No\n: "
    ))

    class StartingOption(Enum):
        Yes = 1
        No = 2

    options = [1, 2]
    if start_input not in options:
        print('Your response must be the numbers 1 or 2\n: ')
        return -1
    else:
        if start_input == 1:
            user_status = StartingOption.Yes
        if start_input == 2:
            user_status = StartingOption.No

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(bank.url)

        # Go to next page
        if user_status is StartingOption.Yes:
            await page.click("#existing_customer")
        else:
            await page.click("#new_customer")

        # Go to next page
        await page.wait_for_selector("button:text('Continue')")
        await page.click("button:text('Continue')")

        await page.wait_for_selector("#first-name")
        await page.fill("#first-name", user.first_name)
        await page.fill("#last-name", user.last_name)

        # Go to next page
        await page.click("button:text('Continue')")
        await page.wait_for_selector("#email-address")

        await page.fill("#email-address", user.contact_info['email'])
        await page.fill("#confirm-email-address", user.contact_info['email'])

        # Go to next page
        await page.click("#button-4")
        await page.wait_for_selector("#mobile-phone-number")

        await page.fill("#mobile-phone-number", user.contact_info['phone_number'])

        # Go to next page
        await page.click("#button-6")
        await page.wait_for_selector("#primary-street")

        await page.fill('#primary-street', user.contact_info['address'])
        # TODO: apt or suite option
        await page.fill('#primary-city', user.contact_info['city'])
        await page.select_option('#primary-state', user.contact_info['state'])
        await page.fill("#primary-zip-code", user.contact_info['zip'])

        if user.different_mailing_address:
            await page.click("button:text('+ Add mailing address (if different from residential address)')")
            await page.fill('#secondary-street', user.contact_info['address'])
            # TODO: apt or suite option
            await page.fill('#secondary-city', user.contact_info['city'])
            await page.select_option('#secondary-state', user.contact_info['state'])
            await page.fill("#secondary-zip-code", user.contact_info['zip'])
        await page.click("button:text('Continue')")

        # Go to next page
        await page.wait_for_selector("button:text('Continue')")
        await page.click("button:text('Continue')")

        # TODO: specific employment status
        if user.employment_info['employed']:
            await page.click("#button-0")
        else:
            await page.click('#button-4')

        # TODO: greater option support instead of hardcoded
        await page.select_option("#job-title", "Engineer/Scientist")

        # Go to next page
        await page.wait_for_selector("button:text('Continue')")
        await page.click("button:text('Continue')")

        salary = int(user.employment_info['annual_income'])
        if salary == 0:
            await page.click("button:text('No income')")
        elif salary <= 50000:
            await page.click("button:text('$1 - $50,000')")
        elif salary <= 100000:
            await page.click("button:text('$50,000 - $100,000')")
        elif salary <= 150000:
            await page.click("button:text('$100,000 - $150,000')")
        elif salary <= 250000:
            await page.click("button:text('$150,000 - $250,000')")
        else:
            await page.click("button:text('Over $250,000')")

        await page.click("button:text('Continue')")

        # Go to next page
        await page.wait_for_selector("#date-of-birth")
        await page.fill("#date-of-birth", user.date_of_birth.replace("-", ""))
        await page.fill("#ssn-or-itin", user.ssn)
        await page.click("button:text('Continue')")

        await page.wait_for_selector("p:text('I certify the following:')")
        await page.click("p:text('I certify the following:')")
        await page.click("button:text('Continue')")

        await page.wait_for_selector("label[for='ods-radio-2-input']")
        await page.click("label[for='ods-radio-2-input']")
        await page.click("button:text('Continue')")

        # Go to next page
        await page.wait_for_selector("label[for='withholding-no-input']")
        if user.tax_info['withholding']:
            await page.click("label[for='withholding-yes-input']")
        else:
            await page.click("label[for='withholding-no-input']")
        await page.click("label[for='ods-checkbox-6-input']")
        await page.click("button:text('Continue')")

        # Go to next page
        await page.wait_for_selector("#fund-later-button")
        await page.click("#fund-later-button")

        # Go to next page
        await page.wait_for_selector("#button-open-account")
        await page.click("#button-open-account")

        input('Account ready.')
        # Go to next page, finish submit.
        await page.wait_for_selector("#button-0")
        await page.click("#button-0")

        time.sleep(999)


async def amex_signup(info):
    bank = SignUp("American Express",
                  "https://www.americanexpress.com/en-us/banking/personal/savings/apply/psa-begin?product=highYieldSavings&intlink=savingshysa-hero-apply")
    user = User(info)
    print("Are you a current American Express Customer?")
    start_input = int(input(
        "1: Yes, I'm a current Card Member\n2: Yes, I'm a Savings Account holder only \n3: No, but I would like to "
        "open a new Savings Account (choose this one for now)\n: "))

    class StartingOption(Enum):
        CardCustomer = 1
        SavingsCustomer = 2
        NewAccount = 3

    options = [1, 2, 3]
    if start_input not in options:
        print('Your response must be the numbers 1, 2, or 3.')
        return -1
    else:
        if start_input == 1:
            user_status = StartingOption.CardCustomer
        if start_input == 2:
            user_status = StartingOption.SavingsCustomer
        if start_input == 3:
            user_status = StartingOption.NewAccount

    # Begin Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(bank.url)

        if user_status is StartingOption.CardCustomer:
            await page.click("label[for='isCardCustomer']")
        elif user_status is StartingOption.NewAccount:
            await page.click("label[for='isNewAccount']")
        elif user_status is StartingOption.SavingsCustomer:
            await page.click("label[for='isSavingsCustomer']")

        # Go to next page
        await page.click("button[id='submit-button']")
        # Wait until next options are available
        await page.wait_for_selector("label[for='noJointUser']", timeout=60000)  # Wait for 60 seconds
        await page.click("label[for='noJointUser']")

        # Go to next page
        await page.click("button[id='submit-button']")
        await page.wait_for_selector("input[id='firstName']")

        # Begin filling in account details
        await page.fill("#firstName", user.first_name)
        await page.fill("#lastName", user.last_name)  # TODO: add middle name support
        # TODO: suffix support (Sr, Jr, III, etc)
        await page.fill("#dateOfBirth", user.date_of_birth.replace("-", ""))
        await page.fill('#taxIdentificationNumber', user.ssn.replace("-", ""))

        # Go to next page
        await page.click("button[id='submit-button']")
        await page.wait_for_selector("#email")

        await page.fill('#email', user.contact_info['email'])
        await page.fill('#phone', user.contact_info['phone_number'])

        if user.uses_paper:
            await page.click("label[for='ELECTRONIC_AND_PAPER']")
        else:
            await page.click("label[for='ELECTRONIC_ONLY']")

        # Go to next page
        await page.click("button[id='submit-button']")
        await page.wait_for_selector("input[id='line1']")

        await page.fill('#line1', user.contact_info['address'])  # street address
        await page.fill('#city', user.contact_info['city'])  # street address
        # TODO: appt, suite #
        await page.select_option("#region", convert_tag(user.contact_info['state']))
        await page.fill('#postalCode', user.contact_info['zip'])  # street address

        if user.different_mailing_address:
            await page.click("label[for='differentMailingAddress']")
            await page.fill('#mailingLine', user.mailing_info['address'])  # street address
            # TODO: appt, suite #
            await page.fill('#mailingCity', user.mailing_info['city'])  # street address
            await page.select_option("#mailingState", convert_tag(user.mailing_info['state']))
            await page.fill('#mailingZip', user.mailing_info['zip'])  # street address

        # Go to next page
        await page.click("button[id='submit-button']")
        await page.wait_for_selector("select[id='employmentStatus']")

        if user.employment_info['employed']:
            await page.select_option('#employmentStatus', 'Employed')
            await page.select_option('#occupation', user.employment_info['occupation'])
        else:
            await page.select_option('#employmentStatus', 'Unemployed')
        await page.fill("#amount", user.employment_info['annual_income'])

        # Go to next page
        await page.click("button[id='submit-button']")
        await page.wait_for_selector("label[for='noTaxWithholdings']", timeout=1000 * 999)

        if user.tax_info['withholding']:
            await page.click("label[for='haveTaxWithholdings']")
        else:
            await page.click("label[for='noTaxWithholdings']")

        # Go to next page
        await page.click("button[id='submit-button']")
        await page.wait_for_selector("button:text('Submit')", timeout=1000 * 999)

        input('Account is ready.')

        time.sleep(3)
        await browser.close()


if __name__ == '__main__':
    with open('account_information.json', 'r') as outfile:
        data = json.load(outfile)
    # asyncio.run(amex_signup(data))
    asyncio.run(capital_one_signup(data))
