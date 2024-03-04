from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def has_login_features(html):
    """
    Checks the provided HTML for login features.
    Looks for input fields that could indicate a login form.
    """
    soup = BeautifulSoup(html, "html.parser")
    # Look for input fields that are commonly used in login forms.
    if soup.find('input', {'type': 'password'}) or soup.find('input', {'name': 'username'}) or soup.find('input', {
        'name': 'sso'}):
        return True
    return False


def take_screenshot(driver, domain):
    """
    Takes a screenshot of the current page and saves it with a filename based on the domain.
    """
    # Sanitize the domain to create a valid filename.
    filename = domain.replace("http://", "").replace("https://", "").replace("www.", "").replace("/", "_") + ".png"
    driver.save_screenshot(filename)
    print(f"Screenshot and URL saved for {domain}")


def check_login_pages(filename):
    """
    Reads domain names from a file and checks each for login pages.
    Takes a screenshot of pages with login features.
    """
    # Initialize the Chrome WebDriver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    with open(filename, 'r') as file:
        for line in file:
            domain = line.strip()
            if not domain.startswith('http'):
                domain = 'https://' + domain
            print(f"Checking {domain}...")

            try:
                driver.get(domain)
                time.sleep(5)  # Wait for the page to fully load.

                html = driver.page_source
                if has_login_features(html):
                    take_screenshot(driver, domain)
                else:
                    print("No login page found for " + domain)

            except Exception as e:
                print(f"Error accessing {domain}: {e}")

    driver.quit()


if __name__ == "__main__":
    filename = "domains.txt"  # Make sure this file exists in the same directory with domain names listed.
    check_login_pages(filename)
