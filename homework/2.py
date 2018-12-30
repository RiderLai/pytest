from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import time


def get_goods(driver, n):
    time.sleep(3)
    try:
        goods = driver.find_elements_by_class_name('gl-item')

        for good in goods:

            detail_url = good.find_element_by_tag_name('a').get_attribute('href')
            photo = good.find_element_by_css_selector('.p-img img').get_attribute('src')
            if photo is None:
                photo = good.find_element_by_css_selector('.p-img img').get_attribute('data-lazy-img')
            # time.sleep(1)
            if not photo.startswith('http'):
                photo = 'http:' + photo
            p_name = good.find_element_by_css_selector('.p-name em').text.replace('\n', '')
            price = good.find_element_by_css_selector('.p-price i').text
            p_commit = good.find_element_by_css_selector('.p-commit a').text
            import requests
            import os

            re = requests.get(photo)
            path_page = os.path.join('download', str(n))
            if not os.path.exists(path_page):
                os.makedirs(path_page)
            path = os.path.join(path_page, str(time.time()) + '.jpg')
            with open(path, 'wb') as f:
                f.write(re.content)
            msg = '''
            商品 : %s
            链接 : %s
            价钱 ：%s
            评论 ：%s
            图片：%s
            ''' % (p_name, detail_url, price, p_commit, photo)

            print(msg, end='\n\n')

        button = driver.find_element_by_partial_link_text('下一页')
        button.click()
        time.sleep(1)
        n += 1
        get_goods(driver, n)
    except Exception as e:
        print(e)


def spider(url, keyword):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(3)  # 使用隐式等待
    try:
        input_tag = driver.find_element_by_id('key')
        input_tag.clear()
        input_tag.send_keys(keyword)
        input_tag.send_keys(Keys.ENTER)
        n = 1
        get_goods(driver, n)

    finally:
        driver.close()


if __name__ == '__main__':
    A = input('请输入关键字')
    spider('https://www.jd.com/', keyword=A)
