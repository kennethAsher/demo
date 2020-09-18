
from selenium import webdriver
from time import sleep

browser = webdriver.Chrome("C://Users//kenneth//chromedriver")
browser.get("https://www.baidu.com")

# browser.find_element_by_id("kw").send_keys("selenium")
#
# browser.find_element_by_id("su").click()
#
# sleep(1)
#
# #1.定位一组元素
# elements = browser.find_elements_by_xpath('//div/h3/a')
# print(elements)
#
# #2.循环遍历出每一条搜索结果的标题
# for t in elements:
#     print(t.text)
#     element = browser.find_element_by_link_text(t.text)
#     element.click()
#     sleep(3)


