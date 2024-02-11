import undetected_chromedriver.v2 as uc
import csv
from bs4 import BeautifulSoup
import time
import LinkedIn_API

def setup_browser():
    # Setup undetected_chromedriver
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # For headless operation
    # Additional options and preferences as needed
    driver = uc.Chrome(options=options)
    return driver

def login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)  # Wait for page to load; adjust as necessary
    driver.find_element_by_id("username").send_keys(email)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(3)  # Wait for potential redirects and full page load

def search_users(driver, query):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(5)  # Wait for search results to load

def scrape_and_save(driver, filename="linkedin_data.csv"):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    profiles = []  # Extracting names and headlines; adapt based on actual page structure
    # Note: Page structure may have changed, adjust selectors accordingly
    for profile in soup.find_all("div", class_="search-result__info"):
        try:
            name = profile.find("span", class_="name actor-name").get_text(strip=True)
            headline = profile.find("p", class_="subline-level-1").get_text(strip=True)
            profiles.append((name, headline))
        except AttributeError:
            continue  # Skip profiles that don't match the expected structure

    # Save the first 5 profiles to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Headline"])  # Headers
        writer.writerows(profiles[:5])  # Save only the first 5 profiles

if __name__ == "__main__":
    driver = setup_browser()
    login(driver, "email@gmail.com", "password")  # Replace with actual details
    search_users(driver, "Rahul Singh")
    scrape_and_save(driver)
    driver.quit()
