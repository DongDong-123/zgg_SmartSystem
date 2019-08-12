from selenium import webdriver
from readConfig import ReadConfig
import unittest
from selenium.webdriver.chrome.options import Options
import random
import re
from front_login import *
import time
import HTMLTestRunner
import HtmlTestRunner
from HTMLTestRunner_PY3 import HTMLTestRunner


# 处理价格
def process_price(price):
    if isinstance(price, str):
        if "面议" in price:
            return 0
        elif '￥' or '¥' or '元' in price:
            patt = "['￥','¥','元']"
            return re.sub(patt, "", price)
        else:
            try:
                eval(price)
                return price
            except SyntaxError as e:
                print("价格错误：", e)
                return 0
    elif isinstance(price, float):
        return price
    elif isinstance(price, int):
        return price


class Trademark:
    def __init__(self):
        self.timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    # noinspection PyAttributeOutsideInit
    def trademark_list(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # self.driver = webself.driver.Chrome()
        self.driver.maximize_window()
        # 进入列表页
        self.driver.get(ReadConfig().get_trademark_url())
        list_title = self.driver.title
        print(list_title)

        num = random.randint(1, 20)  # 随机选择一个商标
        # num = 5
        # 获取商标名称、大类、价格
        self.goods_name = self.driver.find_element_by_xpath(".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/p".format(num)).text
        self.goods_type = self.driver.find_element_by_xpath(".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/h2".format(num)).text
        self.goods_price = self.driver.find_element_by_xpath(".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/span".format(num)).text
        self.goods_price = process_price(self.goods_price)
        # 打印参数
        print([self.goods_name, self.goods_type, self.goods_price])

        self.driver.find_element_by_xpath(".//div[@class='tm-mark-pro-item']/ul/li[{}]/a".format(num)).click()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        detail_title = self.driver.title
        print(detail_title)
        self.goods_name2 = self.driver.find_element_by_xpath(".//div[@class='title']/h2").text
        self.goods_type2 = self.driver.find_element_by_xpath(".//table[@class='tm-mark-detai-table']/tbody/tr[1]/td[2]").text
        self.goods_price2 = self.driver.find_element_by_xpath(".//div[@class='tm-mark-detail-money']/div/span/em").text
        print([self.goods_name2, self.goods_type2, self.goods_price2])
        global detail_url
        detail_url = self.driver.current_url
        print("打印", detail_url)
        self.driver.quit()
        return [self.goods_name, self.goods_type, self.goods_price], [self.goods_name2, self.goods_type2, self.goods_price2]

    def trademark_order(self):
        self.driver = front_login(ReadConfig().get_user(), ReadConfig().get_password())
        self.driver.get(detail_url)
        self.driver.maximize_window()

        print(self.driver.current_url)
        print(self.driver.title)
        # 点击立即购买
        self.driver.find_element_by_xpath(".//div[@id='productId']/a[1]").click()

        locator_for_order = (By.XPATH, ".//tbody/tr[@class='tr-comm']/td[1]")
        WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable(locator_for_order))
        # 提取商标信息
        self.goods_type4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[1]").text
        self.goods_name4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[2]").text
        self.goods_code4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[3]").text
        self.goods_price4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[4]").text
        self.goods_offical4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[5]").text
        self.goods_total_price1 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[6]").text

        # 处理价格
        self.goods_total_price2 = self.driver.find_element_by_xpath(".//div[@class='fwfBox']//div/em").text
        self.goods_total_price2 = process_price(self.goods_total_price2)

        self.goods_total_price3 = self.driver.find_element_by_xpath(".//div[@class='totalPrice']//div/b").text
        self.goods_total_price3 = process_price(self.goods_total_price3)

        print(self.goods_type4, self.goods_name4, self.goods_code4, self.goods_price4, self.goods_offical4,
              self.goods_total_price1, self.goods_total_price2, self.goods_total_price3)

        # 下单
        self.driver.find_element_by_xpath(".//a[@id='lnkPay']").click()

        # 获取余额
        get_balance = self.driver.find_element_by_xpath(".//div[@class='balance-radio']//span").text
        get_balance = process_price(get_balance)

        # 选择余额支付
        # self.driver.find_element_by_xpath(".//div[@class='balance-radio']//span").click()

        # 已使用余额
        used_balance = self.driver.find_element_by_xpath(".//label[@id='lbbalance']").text
        used_balance = process_price(used_balance)
        # used_balance = 0

        # 选择支付宝支付
        self.driver.find_element_by_xpath(".//div[@id='zfbzf']/a[@dataid='1']").click()
        # 选择微信支付
        # self.driver.find_element_by_xpath(".//div[@id='zfbzf']/a[@dataid='4']").click()

        # 获取所有显示价格
        goods_pay_price1 = self.driver.find_element_by_xpath(".//div[@class='fwfBox']/div/div[1]/em").text
        goods_pay_price1 = process_price(goods_pay_price1)

        goods_pay_for_balance = self.driver.find_element_by_xpath(".//div[@class='fwfBox']/div/div[2]/em").text
        goods_pay_for_balance = process_price(goods_pay_for_balance)

        goods_pay_price2 = self.driver.find_element_by_xpath(".//div[@class='fwfBox']/div/div[3]/em").text
        goods_pay_price2 = process_price(goods_pay_price2)

        goods_pay_price3 = self.driver.find_element_by_xpath(".//div[@class='top']/b").text
        goods_pay_price3 = process_price(goods_pay_price3)

        print([goods_pay_price1, goods_pay_for_balance, goods_pay_price2, goods_pay_price3, get_balance, used_balance])

        # 支付
        self.driver.find_element_by_xpath(".//a[@id='lnkPay']").click()
        # 判断支付总金额是否为0
        if float(goods_pay_price3):
            # 进入二维码页面
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])

            path = "screen/screen{}.png".format(self.timetemp)
            # 等待二维码加载
            locator_for_QR = (By.XPATH, "//canvas")
            WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable(locator_for_QR))

            QR_price1 = self.driver.find_element_by_xpath(".//span[@id='J_basePriceArea']/strong").text
            QR_price2 = self.driver.find_element_by_xpath(".//div[@class='qrcode-header']/div[2]").text

            # 截图
            self.driver.save_screenshot(path)
            time.sleep(0.5)
            self.driver.close()
            self.driver.switch_to.window(windows[0])
            # 点击已完成支付
            self.driver.find_element_by_xpath(".//div[@class='wczfBtn']/input").click()
            print([QR_price1, QR_price2])

        else:
            QR_price1, QR_price2 = 0, 0
            sleep(0.5)
            path = "screen/Sucess{}.png".format(self.timetemp)
            self.driver.save_screenshot(path)

            submit_status = self.driver.find_element_by_xpath(".//div[@class='comm']/p").text
            self.driver.find_element_by_link_text(u"确定").click()
            print('submit_status', submit_status)
            self.driver.get("https://user.zgg.com/user/market/order.html")

        # 进入个人中心，等待页面加载完毕
        locator_for_case = (By.XPATH, "//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td[2]/a[1]")
        WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable(locator_for_case))

        # 获取案件信息
        goods_order_number = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[1]/td/span[1]").text
        # goods_order_number = goods_order_number.replace("订单号：", "")
        pay_state = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[1]/td/span[3]").text

        goods_name_in_case = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td/span[1]").text
        goods_name_in_case = goods_name_in_case.replace("商品名称:", "")
        goods_type_in_case = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td/span[2]").text
        goods_type_in_case = goods_type_in_case.replace("商品分类:", "")

        goods_case_code = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td/span[3]").text
        goods_case_code = goods_case_code.replace("案件编号:", "").strip()
        goods_case_price = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td[4]/span").text

        print([goods_order_number, pay_state, goods_name_in_case, goods_case_code, goods_case_price])

        return ([self.goods_name4, self.goods_type4, self.goods_price4, self.goods_code4, self.goods_offical4,
              self.goods_total_price1, self.goods_total_price2, self.goods_total_price3], [QR_price1, QR_price2],
            [goods_pay_price1, goods_pay_for_balance, goods_pay_price2, goods_pay_price3, get_balance, used_balance],
            [goods_order_number, pay_state, goods_name_in_case, goods_type_in_case, goods_case_code, goods_case_price])

