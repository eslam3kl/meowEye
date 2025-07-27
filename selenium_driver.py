from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import tldextract
from config import color_tag

def create_driver(user_url, proxy=None):
    chrome_options = Options()
    if user_url.startswith("https://"):
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")

    seleniumwire_options = {'verify_ssl': False}

    if proxy:
        seleniumwire_options['proxy'] = {
            'http': proxy,
            'https': proxy,
            'no_proxy': 'localhost,127.0.0.1'
        }
        print(f"{color_tag('[info]')} Using proxy: {proxy}")
    else:
        print(f"{color_tag('[WAR]')} No proxy set, proceeding without proxy")

    driver = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=chrome_options)
    return driver

def request_in_scope(request, target_root_domain):
    parsed = urlparse(request.url)
    ext = tldextract.extract(parsed.netloc)
    request_root_domain = f"{ext.domain}.{ext.suffix}"
    return request_root_domain == target_root_domain
