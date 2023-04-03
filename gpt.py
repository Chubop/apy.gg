import os
import openai
import re

openai.api_key = "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"
raw_text = "[('4.00', 'ions. 4.00 % apy* no'), ('4.00', 'ions. 4.00 % apy* no'), ('4.00', 'hrony 4.00 % apy* $5'), ('4.00', 'hrony 4.00 % apy* $5'), ('0.02', 'chase 0.02 % apy* $5'), ('0.02', 'chase 0.02 % apy* $5'), ('0.01', ' bank 0.01 % apy* $5'), ('0.01', ' bank 0.01 % apy* $5'), ('0.32', 'erage 0.32 % apy* $5'), ('0.32', 'erage 0.32 % apy* $5'), ('4.00', 'hrony 4.00 % apy* $5'), ('4.00', 'hrony 4.00 % apy* $5'), ('0.02', 'chase 0.02 % apy* $5'), ('0.02', 'chase 0.02 % apy* $5'), ('0.01', ' bank 0.01 % apy* $5'), ('0.01', ' bank 0.01 % apy* $5'), ('0.32', 'erage 0.32 % apy* $5'), ('0.32', 'erage 0.32 % apy* $5'), ('4.00%', ',999 4.00% apy* depo'), ('4.00%', ',999 4.00% apy* depo'), ('4.00%', ',999 4.00% apy* depo'), ('4.00%', ',999 4.00% apy* depo'), ('4.00%', '.01+ 4.00% apy* open'), ('4.00%', '.01+ 4.00% apy* open'), ('2.25%', 'mas) 2.25% apy* no m'), ('2.25%', 'mas) 2.25% apy* no m'), ('4.50%', 'cds) 4.50% apy* at 1'), ('4.50%', 'cds) 4.50% apy* at 1')]"
def get_apy(raw_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{
            "role": "user",
            "content": "The following list is from scraped HTML of a bank's savings accounts page "
                       "Each entry is stored as a"
                       "tuple, the first being the value, and the second being the nearby text +-50 characters. I'm "
                       "trying to scrape the main APY% from this list, but I'm having trouble with false positives. "
                       "Could you tell me what the correct APY% is from this list? Please just return the float as your response, "
                       "do not include any letters. Here's the list: {}".format(raw_text)
        }],
    )
    answer = (completion['choices'][0]['message']['content'])
    pattern = r"\d+\.\d+"
    match = re.search(pattern, answer)
    return float(match.group())


if __name__ == '__main__':
    print(get_apy(raw_text))
