from selenium import webdriver


def chrome_browser(download_dir=''):

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", {
      "download.default_directory" : download_dir,
      #'profile.default_content_setting_values.automatic_downloads': 2,
      "download.prompt_for_download": False,
      "download.directory_upgrade": False,
      "excludeSwitches": ["enable-automation"],
      'useAutomationExtension' :False,
      "safebrowsing.enabled": True
    })

    chromedriver="C:\\Users\\Rafael Monroig\\git\\z_drivers\\chromedriver"
    browser = webdriver.Chrome(chromedriver, chrome_options=chromeOptions)

    return browser


def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
