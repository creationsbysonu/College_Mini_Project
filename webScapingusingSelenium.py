from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

# Setting up the Selenium WebDriver with SSL handling
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
driver = webdriver.Chrome(options=options)

# URL of the product page
url = "https://www.daraz.com.np/products/earphone-with-mic-for-android-ios-smartphones-i101108192-s1021676682.html?pvid=f6613d04-66cd-475e-b346-b834b660322f&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335409.just4u.d_101108192"
driver.get(url)

# Waiting for the reviews tab to load and click it
try:
    print("Waiting for the reviews tab to load...")
    reviews_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review_star_1"]/div/a')) # X-path khojne inspect garera yesma chai review section lai click garna X-path liyera kholne try gareko ho 
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", reviews_tab)
    time.sleep(1)

    try:
        reviews_tab.click()
        print("Reviews tab clicked.")
    except Exception as e:
        print(f"Click intercepted: {e}. Using JavaScript click instead.")
        driver.execute_script("arguments[0].click();", reviews_tab)
except Exception as e:
    print(f"Error: Could not locate or click the reviews tab: {e}")
    driver.quit()
    exit()

# Waiting for the reviews section to load
try:
    print("Waiting for the reviews section to load...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "mod-reviews"))
    )
    print("Review section loaded.")
except Exception as e:
    print(f"Error: Reviews section not found or failed to load: {e}")
    driver.quit()
    exit()

# Initializing the CSV file and write header
file_path = "reviews.csv"

# Creates the file and writes the header if it doesn't exist
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["reviewText", "reviewDate", "authorName"]) #yesle chai hamro csv file ko header dinxa

# main scarping yaha bata hunxa
page_number = 1
while True:
    print(f"Scraping reviews from page {page_number}...")
    reviews = []
    try:
        review_elements = driver.find_elements(By.CLASS_NAME, "item")  # yo class name chai review section ko ho
        print(f"Found {len(review_elements)} reviews on page {page_number}.")

        for review in review_elements:
            try:
                #hamilai classname chainxa kun kun data scrape garne ho vanera 
                review_text = review.find_element(By.CLASS_NAME, "content").text  # same review section ko item vitra ko class name yaha janxa (yesma chai juun classname le review text dinxa tyo line)
                review_date = review.find_element(By.CLASS_NAME, "top").text  # same yesma review date ko classname halne ho
                author_name = review.find_element(By.CLASS_NAME, "middle").text  # author name (consumer) ko classname halne ho
                reviews.append([review_text, review_date, author_name])
            except Exception as e:
                print(f"Error extracting review data: {e}")
                continue

        # Append reviews to the CSV file
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for review in reviews:
                writer.writerow(review)

        print(f"Reviews from page {page_number} saved to {file_path}.")
    except Exception as e:
        print(f"Error finding review elements on page {page_number}: {e}")

    # Moving to the next page
    try:
        # Waiting for the "Next" button to be clickable
        # yaha 10 chai maximum no. of seconds ho wait garne yadi teti time ma khulena vane timeout error message aauxu
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]'))
        )
        
        # Scroll into view to avoid overlap
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

        # Checking if the "Next" button is disabled
        if "disabled" in next_button.get_attribute("class"):
            print("No more pages. Exiting pagination.")
            break
        
        # Using JavaScript to click the "Next" button
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # Allowing time for the next page to load
        page_number += 1

    except Exception as e:
        print(f"Error finding or clicking the 'Next' button: {e}")
        break  # Exiting the loop if the "Next" button is not found or click fails

# Closing the browser
driver.quit()
print("Scraping completed.")


## If you want to customize the number of reviews to scrape then use this code : 
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import csv

# # Setting up the Selenium WebDriver with SSL handling
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
# driver = webdriver.Chrome(options=options)

# # URL of the product page
# url = "https://www.daraz.com.np/products/earphone-with-mic-for-android-ios-smartphones-i101108192-s1021676682.html?pvid=f6613d04-66cd-475e-b346-b834b660322f&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335409.just4u.d_101108192"
# driver.get(url)

# # Waiting for the reviews tab to load and click it
# try:
#     print("Waiting for the reviews tab to load...")
#     reviews_tab = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review_star_1"]/div/a'))
#     )
#     driver.execute_script("arguments[0].scrollIntoView(true);", reviews_tab)
#     time.sleep(1)

#     try:
#         reviews_tab.click()
#         print("Reviews tab clicked.")
#     except Exception as e:
#         print(f"Click intercepted: {e}. Using JavaScript click instead.")
#         driver.execute_script("arguments[0].click();", reviews_tab)
# except Exception as e:
#     print(f"Error: Could not locate or click the reviews tab: {e}")
#     driver.quit()
#     exit()

# # Waiting for the reviews section to load
# try:
#     print("Waiting for the reviews section to load...")
#     WebDriverWait(driver, 30).until(
#         EC.presence_of_all_elements_located((By.CLASS_NAME, "mod-reviews"))
#     )
#     print("Review section loaded.")
# except Exception as e:
#     print(f"Error: Reviews section not found or failed to load: {e}")
#     driver.quit()
#     exit()

# # Initializing the CSV file and write header
# file_path = "reviews.csv"

# # Creates the file and writes the header if it doesn't exist
# with open(file_path, mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["REVIEW_TEXT", "REVIEW_DATE", "AUTHOR_NAME"])

# # Main scraping process
# page_number = 1
# max_pages = 20  # Limit to scrape only 20 pages

# while page_number <= max_pages:
#     print(f"Scraping reviews from page {page_number}...")
#     reviews = []
#     try:
#         review_elements = driver.find_elements(By.CLASS_NAME, "item")  # Class name for review items
#         print(f"Found {len(review_elements)} reviews on page {page_number}.")

#         for review in review_elements:
#             try:
#                 # Extracting review data
#                 review_text = review.find_element(By.CLASS_NAME, "content").text
#                 review_date = review.find_element(By.CLASS_NAME, "top").text
#                 author_name = review.find_element(By.CLASS_NAME, "middle").text
#                 reviews.append([review_text, review_date, author_name])
#             except Exception as e:
#                 print(f"Error extracting review data: {e}")
#                 continue

#         # Append reviews to the CSV file
#         with open(file_path, mode="a", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerows(reviews)

#         print(f"Reviews from page {page_number} saved to {file_path}.")

#     except Exception as e:
#         print(f"Error finding review elements on page {page_number}: {e}")

#     # Moving to the next page
#     try:
#         next_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]'))
#         )
        
#         # Scroll into view to avoid overlap
#         driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

#         # Check if the "Next" button is disabled
#         if "disabled" in next_button.get_attribute("class"):
#             print("No more pages. Exiting pagination.")
#             break

#         # Click the "Next" button
#         driver.execute_script("arguments[0].click();", next_button)
#         time.sleep(3)  # Allow time for the next page to load
#         page_number += 1

#     except Exception as e:
#         print("No more pages or navigation issue. Exiting pagination.")
#         break

# # Closing the browser
# driver.quit()
# print("Scraping completed.")
