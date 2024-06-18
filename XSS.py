import sys
from bs4 import BeautifulSoup
import requests
import html

# Function to fetch HTML content from a URL
def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Function to detect specific XSS payloads using BeautifulSoup
def detect_xss(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all script tags in the HTML
    script_tags = soup.find_all('script')

    # Check if any script tags contain known XSS payloads
    for script_tag in script_tags:
        script_content = script_tag.get_text()
        if "function MM_reloadPage(init)" in script_content:
            return "alert('hEYYO XSS Vuln Detected!')"  # Return the simplified XSS payload
    
    return None  # No XSS vulnerability detected

# Function to scan a URL for XSS vulnerabilities
def scan_for_xss(url):
    html_content = fetch_html_content(url)
    if html_content:
        xss_script = detect_xss(html_content)
        if xss_script:
            print(f"Script causing XSS: {xss_script}")
            print(f"Potential XSS vulnerability detected in: {url}")
        else:
            print(f"No XSS vulnerability detected in: {url}")
    else:
        print(f"Failed to fetch HTML content from: {url}")

# Function to print ASCII art once code is launched
def print_ascii_art():
    ascii_art = """

░       ░░░░      ░░░   ░░░  ░░        ░░░      ░░░  ░░░░  ░░  ░░░░  ░░░      ░░░░      ░░
▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒    ▒▒  ▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒  ▒▒  ▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒
▓       ▓▓▓  ▓▓▓▓  ▓▓  ▓  ▓  ▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓▓▓    ▓▓▓▓▓      ▓▓▓▓      ▓▓
█  ████████        ██  ██    █████  █████        ██  ████  ███  ██  █████████  ████████  █
█  ████████  ████  ██  ███   █████  █████  ████  ███      ███  ████  ███      ████      ██
                                                                                          
     Developed by Perthlis
    """
    print(ascii_art)

# Main execution when script is run
if __name__ == "__main__":
    print_ascii_art()

    # Check if a URL argument is provided via command-line
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        # Prompt user to enter the target URL manually
        target_url = input("Enter the URL to scan for XSS vulnerabilities: ")

    # Perform XSS scan on the provided target URL
    scan_for_xss(target_url)
