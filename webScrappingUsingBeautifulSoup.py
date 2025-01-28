import requests
from bs4 import BeautifulSoup
import csv
import time

# URL of the product page
url = "https://www.daraz.com.np/products/earphone-with-mic-for-android-ios-smartphones-i101108192-s1021676682.html"

# Fetch the page content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch page content. Status code: {response.status_code}")
    exit()

# Parse the page with Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize the CSV file
file_path = "reviews.csv"
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Review Text", "Review Date", "Author Name"])

# Find and extract reviews
page_number = 1
while True:
    print(f"Scraping reviews from page {page_number}...")

    # Adjust the following selectors based on the actual page structure
    reviews = soup.find_all("div", class_="mod-reviews")
    if not reviews:
        print("No more reviews found. Exiting.")
        break

    review_data = []
    for review in reviews:
        try:
            review_text = review.find("div", class_="content").get_text(strip=True)
            review_date = review.find("div", class_="top").get_text(strip=True)
            author_name = review.find("div", class_="middle").get_text(strip=True)
            review_data.append([review_text, review_date, author_name])
        except AttributeError as e:
            print(f"Error extracting review data: {e}")
            continue

    # Write reviews to the CSV file
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(review_data)

    print(f"Reviews from page {page_number} saved to {file_path}.")

    # Check for a next page
    next_button = soup.find("button", class_="next-button-class")  # Update selector as per the page
    if not next_button or "disabled" in next_button.get("class", []):
        print("No more pages or next button disabled. Exiting.")
        break

    # Simulate a next-page request (requires modifying URL or POST request if pagination exists)
    # Example assumes `page_number` is part of the query string
    page_number += 1
    time.sleep(2)  # Pause to avoid overloading the server
    next_page_url = f"{url}?page={page_number}"  # Adjust based on pagination structure
    response = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

print("Scraping completed.")
