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
url = "https://www.daraz.com.np/products/asitis-creatine-monohydrate-100g-33-servings-labdoor-usa-certified-for-accuracy-purity-i179779770-s1209671636.html?scm=1007.51610.379274.0&pvid=75b175b6-361f-4d1e-8681-7fe6825df094&search=flashsale&spm=a2a0e.tm80335409.FlashSale.d_179779770"
driver.get(url)

try:
    # Step 2: Wait for the reviews tab to be clickable
    print("Waiting for the reviews tab to load...")
    reviews_tab = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review_star_1"]/div/a'))
    )
    print("Reviews tab located. Scrolling into view...")

    # Scroll to the reviews tab and ensure no overlay blocks it
    driver.execute_script("arguments[0].scrollIntoView(true);", reviews_tab)
    time.sleep(1)  # Allow the scrolling animation to complete

    # Handle potential overlays or sticky headers
    try:
        overlay_close = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'close-overlay-class'))  # Replace with actual class name
        )
        overlay_close.click()
        print("Overlay closed.")
    except Exception:
        print("No overlay found.")

    # Try clicking the tab
    try:
        reviews_tab.click()
        print("Reviews tab clicked.")
    except Exception:
        print("Click intercepted. Attempting JavaScript click...")
        driver.execute_script("arguments[0].click();", reviews_tab)

except Exception as e:
    print(f"Error: Could not locate or click the reviews tab: {e}")
    driver.quit()
    exit()

# Step 3: Wait for the reviews section to load
try:
    print("Waiting for the reviews section to load...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "mod-reviews"))  # Update with the actual class name
    )
    print("Review section loaded.")
except Exception as e:
    print(f"Error: Reviews section not found or failed to load: {e}")
    driver.quit()
    exit()

# Step 4: Scroll the page to load all reviews (if necessary)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)  # Allow time for additional reviews to load

# Step 5: Extract review elements
reviews = []
try:
    review_elements = driver.find_elements(By.CLASS_NAME, "item")  # Replace with actual class name for reviews
    print(f"Found {len(review_elements)} reviews.")

    for review in review_elements:
        try:
            # Replace class names below with the actual class names for review details
            review_rating = review.find_element(By.CLASS_NAME, "top").text
            review_author = review.find_element(By.CLASS_NAME, "middle").text
            review_text = review.find_element(By.CLASS_NAME, "content").text

            # Append review details to the list
            reviews.append({
                "text": review_text,
                "rating": review_rating,
                "author": review_author
            })
        except Exception as e:
            print(f"Error extracting review data: {e}")
            continue
except Exception as e:
    print(f"Error finding review elements: {e}")

# Step 6: Save reviews to a CSV file (with line spacing between reviews)
if reviews:
    file_exists = os.path.isfile("reviews.csv")  # Check if the file already exists

    # for write 'w' and append 'a'
    with open("reviews.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "rating", "author"])
        file.write("REVIEW TEXT, REVIEW DATE, AUTHOR NAME \n") 
        # Write the header only if the file doesn't already exist
        if not file_exists:
            writer.writeheader()

        # Write each review and add a blank line after each review
        for review in reviews:
            writer.writerow(review)  # Write review data
            file.write("\n")  # Add an empty line after each review

    print("Reviews saved to reviews.csv with a blank line between each review.")
else:
    print("No reviews were found.")

# Step 7: Close the browser
driver.quit()
