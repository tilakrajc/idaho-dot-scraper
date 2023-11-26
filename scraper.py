#################################################
# This script scrapes the top 5 postings from   #
# the link below. It uses Selenium to navigate  #
# through the pages and extract the information #
# from the postings and prints it.              #
# Simply run this file.                         #
#################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium webdriver
driver = webdriver.Chrome()

# Open the main page
url = "https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787"
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 1)

postings = []

# Finding the top 5 postings using ID
for i in range(1, 6):
    try:
        posting = wait.until(EC.presence_of_element_located((By.ID, str(i))))
        link = posting.find_element(By.TAG_NAME, "a")
    except Exception:
        print(f"Error: Could not find the posting {i}")
        continue

    # Click on the link while suppressing the error message
    try:
        link.click()
    except Exception:
        print(f"Error: Could not click on the link {i}")
        pass

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "panel")))

    infotable = driver.find_elements(By.CLASS_NAME, "panel")
    table_info = [td.text.strip() for td in infotable[1].find_elements(By.TAG_NAME, "tr")[2].find_elements(By.TAG_NAME, "td")]
    est_value_notes = table_info[1]
    description = infotable[2].find_elements(By.TAG_NAME, "tr")[2].find_elements(By.TAG_NAME, "td")[1].text.strip()
    closing_date = driver.find_element(By.CLASS_NAME, "posting-second-header").find_elements(By.TAG_NAME, "b")[1].text.strip()

    posting_info = {
        "Posting": i,
        "Est. Value Notes": est_value_notes,
        "Description": description,
        "Closing Date": closing_date
    }

    postings.append(posting_info)

    # Return to original page
    driver.get(url)

# Close the Selenium webdriver
driver.quit()

# Print the postings
for posting in postings:
    print(f"Posting {posting['Posting']}:\nEst. Value Notes: {posting['Est. Value Notes']}\nDescription: {posting['Description']}\nClosing Date: {posting['Closing Date']}\n{'-' * 30}")
