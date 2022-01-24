import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# ----- Constants -----
chrome_driver_path = r"C:\Users\elana\Google Drive\Programming\Python\chromedriver.exe"
# Write a source language acronym in small letters like "de" or "nl"
SOURCE_LANGUAGE = "de"
# Write a target language acronym like "cs-CS" or "en-US"
TARGET_LANGUAGE = "en-US"
# Creates a NEW FILE!!!
TARGET_FILE_PATH = "file-translated.txt"
ORIGIN_FILE_PATH = "file.txt"
with open(file=TARGET_FILE_PATH, mode="w", encoding="UTF-8") as new_file:
    new_file.write("")


# Init Selenium
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open Deepl
driver.get("https://www.deepl.com/translator")
time.sleep(4.00)

cookies = driver.find_element(By.CLASS_NAME, "dl_cookieBanner--buttonAll")
cookies.click()
time.sleep(1.50)

# Choose a source language
source_langs = driver.find_element(By.CSS_SELECTOR, "div.lmt__language_select.lmt__language_select--source > button.lmt__language_select__active")
source_langs.click()
time.sleep(0.50)
source_lang = driver.find_element(By.XPATH, f"//*[@dl-test='translator-lang-option-{SOURCE_LANGUAGE}']")
source_lang.click()
time.sleep(0.50)

# Choose a target language
target_langs = driver.find_element(By.CSS_SELECTOR, "div.lmt__language_select.lmt__language_select--target > button.lmt__language_select__active")
target_langs.click()
time.sleep(0.50)
target_lang = driver.find_element(By.XPATH, f"//*[@dl-test='translator-lang-option-{TARGET_LANGUAGE}']")
target_lang.click()
time.sleep(0.50)

with open(file=ORIGIN_FILE_PATH, encoding="UTF-8") as file:
    file_text = file.read()

# Start the process
start_i = 0
while start_i <= len(file_text) - 1:
    text_chunk = ""
    # If the remaining text is longer than 5000, find an end of the last sentence in the chunk
    if len(file_text) > start_i + 5000:
        end_i = start_i + 5000
        looking_for_last_sentence = True
        temp_end_i = end_i
        while looking_for_last_sentence:
            current_two_letters = file_text[temp_end_i - 2:temp_end_i]
            current_three_letters = file_text[temp_end_i - 3:temp_end_i]
            current_four_letters = file_text[temp_end_i - 4:temp_end_i]
            if current_two_letters == ". " or current_three_letters == ".\n" or current_four_letters == "\n\n" \
                    or current_three_letters == '." ' or current_four_letters == '."\n':
                text_chunk = file_text[start_i:temp_end_i]
                looking_for_last_sentence = False
            temp_end_i -= 1
            if temp_end_i == start_i:
                text_chunk = file_text[start_i:end_i]
                looking_for_last_sentence = False
    # If this is the last iteration, get it all.
    else:
        end_i = len(file_text)
        text_chunk = file_text[start_i: end_i]
    start_i += len(text_chunk)
    # Now translate with selenium and deepl
    source = driver.find_element(By.CSS_SELECTOR, "textarea.lmt__textarea.lmt__source_textarea.lmt__textarea_base_style")
    source.send_keys(text_chunk)
    time.sleep(20.00)
    target = driver.find_element(By.XPATH, "//*[@id='target-dummydiv']")
    time.sleep(1.00)
    result = target.get_attribute("textContent")
    # Append the translated text
    with open(file=TARGET_FILE_PATH, mode="a", encoding="UTF-8") as new_file:
        new_file.write(result)
        print(f"One part finished, {start_i-len(file_text)} characters remain to translate.")
    driver.refresh()
    time.sleep(2.00)