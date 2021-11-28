#! python3
""" Opening random video with cat;
    with simple linear execution. """
import sys
import time
import random
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument("start-maximized")
browser = webdriver.Firefox(firefox_options=options)

try:
    browser.get("https://www.google.com/")
    time.sleep(3)
    assert "No results found." not in browser.page_source, "1. Couldn't open www.google.com."
    print("Browser is open.")

    print("Search for the input form:")
    web_form = browser.find_element_by_name("q")
    print(f"\tfound <{web_form.tag_name} {web_form.get_attribute('title')}>;")
    print("\tsending keys...")
    web_form.send_keys("youtube")
    print("\tsubmit the form...")
    web_form.submit()
    time.sleep(3)
    assert "No results found." not in browser.page_source, "2. Fail to submit search form."
    print("Search form found and submitted successfully.")

    print("Search for the youtube:")
    web_link = None
    results = browser.find_elements_by_css_selector('div.g')
    print(f"\tfound {len(results)} div containers;")
    for web_ell in results:
        link = web_ell.find_element_by_tag_name('a')
        if "www.youtube.com/" in link.get_attribute('href'):
            print(f"\tfound <{link.tag_name} {link.get_attribute('href')}>;")
            web_link = link
            break
    print("\tgo to youtube...")
    web_link.click()
    time.sleep(3)
    assert "No results found." not in browser.page_source, "3. Couldn't open www.youtube.com."
    print("Youtube link found and go to the site is successful.")

    print("Search for the input form:")
    web_form = browser.find_element_by_name("search_query")
    print(f"\tfound <{web_form.tag_name} {web_form.get_attribute('placeholder')}>;")
    print("\tsending keys...")
    web_form.send_keys("cat")
    print("\tsubmit the form...")
    web_form.submit()
    time.sleep(3)
    assert "No results found." not in browser.page_source, "4. Fail to submit Youtube form."
    print("Youtube form found and submitted successfully.")

    print("Search for the video:")
    results = browser.find_elements_by_id("video-title")
    print(f"\tfound {len(results)} id's;")
    print("\tchoice the random video...")
    time.sleep(3)
    random.seed()
    web_video = random.choice(results)
    web_video.click()
    time.sleep(3)
    assert "No results found." not in browser.page_source, "5. Video link opening failed."

except Exception as error:
    print("ERROR", error)
    sys.exit(1)
else:
    print("Enjoy your (stupid advertising and) cats!")
    sys.exit(0)
