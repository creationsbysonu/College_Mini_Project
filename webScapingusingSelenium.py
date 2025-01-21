from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

# Step 1: Set up the Selenium WebDriver with SSL handling
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
driver = webdriver.Chrome(options=options)

# URL of the product page
url = "https://www.daraz.com.np/products/earphone-with-mic-for-android-ios-smartphones-i101108192-s1021676682.html?pvid=f6613d04-66cd-475e-b346-b834b660322f&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335409.just4u.d_101108192"
driver.get(url)

# Step 2: Wait for the reviews tab to load and click it
try:
    print("Waiting for the reviews tab to load...")
    reviews_tab = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review_star_1"]/div/a'))
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

# Step 3: Wait for the reviews section to load
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

# Step 4: Initialize the CSV file and write header
file_path = "reviews.csv"

# Create the file and write the header if it doesn't exist
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["REVIEW_TEXT", "REVIEW_DATE", "AUTHOR_NAME"])  # Write the header

# Step 5: Scrape reviews from all pages
page_number = 1
while True:
    print(f"Scraping reviews from page {page_number}...")
    reviews = []
    try:
        review_elements = driver.find_elements(By.CLASS_NAME, "item")  # Update with actual class name
        print(f"Found {len(review_elements)} reviews on page {page_number}.")

        for review in review_elements:
            try:
                review_text = review.find_element(By.CLASS_NAME, "content").text  # Update with actual class name
                review_date = review.find_element(By.CLASS_NAME, "top").text  # Update with actual class name
                author_name = review.find_element(By.CLASS_NAME, "middle").text  # Update with actual class name
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

    # Step 6: Move to the next page
    try:
        # Wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]'))
        )
        
        # Scroll into view to avoid overlap
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

        # Check if the "Next" button is disabled
        if "disabled" in next_button.get_attribute("class"):
            print("No more pages. Exiting pagination.")
            break
        
        # Use JavaScript to click the "Next" button
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # Allow time for the next page to load
        page_number += 1

    except Exception as e:
        print(f"Error finding or clicking the 'Next' button: {e}")
        break  # Exit the loop if the "Next" button is not found or click fails

# Step 7: Close the browser
driver.quit()
print("Scraping completed.")
