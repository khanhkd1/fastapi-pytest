import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


driver = webdriver.Edge()
action = ActionChains(driver)
driver.maximize_window()

# Go to main site
driver.get("https://vnexpress.net/")
time.sleep(10)

# Click to the first post
css_first_post = "article.article-topstory .thumb-art > a"
element_selector = driver.find_elements(By.CSS_SELECTOR, css_first_post)[0]
action.move_to_element(element_selector)
action.click()
action.perform()
time.sleep(10)

# Back to main site
driver.get("https://vnexpress.net/")
time.sleep(10)

css_goc_nhin = "li.gocnhin .thumb-art > a"

driver.close()
