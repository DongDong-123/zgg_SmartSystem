from selenium import webdriver
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from readConfig import ReadConfig
import time
import platform


def front_login(username, password):
    from selenium.webdriver.chrome.options import Options
    if 'Windows' in platform.system():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(r"C:\Users\Dong\AppData\Local\Google\Chrome\Application\chromedriver.exe",
                                  chrome_options=chrome_options)
    elif 'Linux' in platform.system():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('/opt/google/chrome/chromedriver', chrome_options=chrome_options)

    else:
        raise SystemError("系统错误！")

    # jenkins内集成运行时，要指定chromedriver文件的位置
    # driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get(ReadConfig().login_page())

    locator = (By.LINK_TEXT, '密码登录')
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locator))
    driver.find_element_by_link_text(u'密码登录').click()
    # 输入账号、密码、点击登录
    driver.find_element_by_id('tb_user').send_keys(username)
    driver.find_element_by_id('tb_password').send_keys(password)
    driver.find_element_by_id('login1').click()
    # 登录成功
    sleep(4)
    return driver
    # driver.quit()


if __name__ == '__main__':
    front_login('', '')
