from selenium import webdriver
from readConfig import ReadConfig
import unittest
from selenium.webdriver.chrome.options import Options
import random
import re
from front_login import *
import time
from Common_func import *


class Trademark:
    def __init__(self):
        self.timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        self.driver = None

    # noinspection PyAttributeOutsideInit
    def trademark_list(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # self.driver = webdriver.Chrome()
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
        # 进入详情页
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        detail_title = self.driver.title
        print(detail_title)
        self.goods_detail_name = self.driver.find_element_by_xpath(".//div[@class='title']/h2").text
        self.goods_detail_type = self.driver.find_element_by_xpath(".//table[@class='tm-mark-detai-table']/tbody/tr[1]/td[2]").text
        self.goods_detail_price = self.driver.find_element_by_xpath(".//div[@class='tm-mark-detail-money']/div/span/em").text
        print([self.goods_detail_name, self.goods_detail_type, self.goods_detail_price])
        global detail_url
        detail_url = self.driver.current_url
        print("打印", detail_url)
        self.driver.quit()
        return {
            "goods_name": self.goods_name,
            "goods_type": process_type(self.goods_type),
            "goods_price": float(self.goods_price),
            "goods_detail_name": self.goods_detail_name,
            "goods_detail_type": process_type(self.goods_detail_type),
            "goods_detail_price": float(self.goods_detail_price)
        }
    # 提交订单
    def commit_order(self):
        locator = (By.XPATH, "(//parent::li[div[@class='selected-b']])[1]")
        WebDriverWait(self.driver, 30, 1).until(EC.element_to_be_clickable(locator))
        case_name = self.driver.find_element_by_xpath("//tr[@class='tr-comm']/td[1]").text
        case_number = self.driver.find_element_by_xpath("//tr[@class='tr-comm']/td[3]").text
        case_price = self.driver.find_element_by_xpath("//tr[@class='tr-comm']/td[4]").text
        totalprice = self.driver.find_element_by_xpath("//div[@class='totalPrice']/div/b").text
        totalprice = process_price(totalprice)
        self.driver.find_element_by_id('lnkPay').click()
        # 返回价格
        return case_name, case_number, case_price, totalprice

    # 支付
    def pay(self, windows):
        pay_totalprice = self.driver.find_element_by_xpath("//div[@class='totalPrice']/div/b").text
        self.driver.find_element_by_id('lnkPay').click()
        self.driver.switch_to_window(windows[-1])
        self.driver.find_element_by_xpath("//div[@class='wczfBtn']/input").click()
        return process_price(pay_totalprice)


    def trademark_order(self):
        self.driver = front_login(ReadConfig().get_user(), ReadConfig().get_password())
        self.driver.get(detail_url)
        self.driver.maximize_window()

        print(self.driver.current_url)
        print(self.driver.title)
        # 点击立即购买
        self.driver.find_element_by_xpath(".//div[@id='productId']/a[1]").click()
        # 进入下单页
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
        # 进入支付页面
        # 获取可用余额
        get_usable_balance = self.driver.find_element_by_xpath(".//div[@class='balance-radio']//span").text
        get_usable_balance = process_price(get_usable_balance)

        # 选择余额支付
        # self.driver.find_element_by_xpath(".//div[@class='balance-radio']//span").click()


        # 已使用余额
        used_balance = self.driver.find_element_by_xpath(".//label[@id='lbbalance']").text
        used_balance = process_price(used_balance)
        # used_balance = 0

        # 选择支付宝支付
        self.driver.find_element_by_xpath(".//div[@id='zfbzf']/a[@dataid='1']").click()
        pay_state = "支付宝"
        # 选择微信支付
        # self.driver.find_element_by_xpath(".//div[@id='zfbzf']/a[@dataid='4']").click()
        # pay_state = "微信"

        # 获取所有显示价格
        goods_pay_price1 = self.driver.find_element_by_xpath(".//div[@class='fwfBox']/div/div[1]/em").text
        goods_pay_price1 = process_price(goods_pay_price1)

        goods_pay_for_balance = self.driver.find_element_by_xpath(".//div[@class='fwfBox']/div/div[2]/em").text
        goods_pay_for_balance = process_price(goods_pay_for_balance)

        goods_pay_price2 = self.driver.find_element_by_xpath(".//div[@class='fwfBox']/div/div[3]/em").text
        goods_pay_price2 = process_price(goods_pay_price2)

        goods_pay_price3 = self.driver.find_element_by_xpath(".//div[@class='top']/b").text
        goods_pay_price3 = process_price(goods_pay_price3)

        print([goods_pay_price1, goods_pay_for_balance, goods_pay_price2, goods_pay_price3, get_usable_balance, used_balance])

        # 支付
        self.driver.find_element_by_xpath(".//a[@id='lnkPay']").click()

        # 进入二维码页面
        # 判断支付总金额是否为0
        if float(goods_pay_price3):
            # 进入二维码页面
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])

            path = "screen/screen{}.png".format(self.timetemp)
            # 等待二维码加载
            time.sleep(3)
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
            sleep(2)
            path = "screen/Sucess{}.png".format(self.timetemp)
            self.driver.save_screenshot(path)

            submit_status = self.driver.find_element_by_xpath(".//div[@class='comm']/p").text
            # self.driver.find_element_by_link_text(u"确定").click()
            print('submit_status', submit_status)
            self.driver.get("https://user.zgg.com/user/market/order.html")

        # 进入个人中心，等待页面加载完毕
        locator_for_case = (By.XPATH, "//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td[2]/a[1]")
        WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable(locator_for_case))

        # 获取案件信息
        center_order_number = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[1]/td/span[1]").text
        # goods_order_number = goods_order_number.replace("订单号：", "")
        center_pay_state = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[1]/td/span[3]").text

        center_goods_name = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td/span[1]").text
        center_goods_name = center_goods_name.replace("商品名称:", "")
        center_goods_type = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td/span[2]").text
        center_goods_type = center_goods_type.replace("商品分类:", "")

        center_case_code = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td/span[3]").text
        center_case_code = center_case_code.replace("案件编号:", "").strip()
        # 交易状态
        center_case_trade_state = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[2]/tbody[1]/tr[2]/td[3]/div[@class='proess']").text
        center_case_price = self.driver.find_element_by_xpath(
            ".//div[@class='zc-case-table']/table[@class='zc-payment-comm']//tr[2]/td[4]/span").text
        print([center_order_number, center_pay_state, center_goods_name, center_case_code, center_case_price])

        # 商标详情
        self.driver.find_element_by_xpath(
            ".//table[@class='zc-payment-comm']/tbody/tr[2]/td[2]/a[1]").click()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        goods_detail_name2 = self.driver.find_element_by_xpath(".//div[@class='title']/h2").text
        goods_trade_state = self.driver.find_element_by_xpath(".//div[@class='tm-mark-detail-money']/div/span[1]").text
        print("交易状态", goods_trade_state)
        print("goods_detail_name2", goods_detail_name2)
        self.driver.switch_to.window(windows[0])
        # self.driver.close()

        # 订单详情
        self.driver.find_element_by_xpath(".//div[@class='zc-case-table']/table[2]//td[@class='same pay']/a[2]").click()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(1)
        # 支付方式，处理后类型float
        time.sleep(1)

        # locator_for_detail = (By.XPATH, ".//div[@class='caseComm']/div[1]/p[2]")
        # WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable(locator_for_detail))

        order_detail_pay_state = self.driver.find_element_by_xpath(
            ".//div[@class='caseComm']/div[1]/p[2]").text
        order_detail_pay_state = process_order_infos(order_detail_pay_state)
        # order_detail_pay_state = "支付宝"
        # 总费用，处理后类型float
        order_detail_total_price = self.driver.find_element_by_xpath(
            ".//div[@class='caseComm']/div[1]/p[3]/span").text
        order_detail_total_price = turn_to_float(get_price(order_detail_total_price)[0])
        # 红包支付金额,处理后类型float
        order_detail_red_packet = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[1]/p[4]").text
        order_detail_red_packet = turn_to_float(get_price(order_detail_red_packet)[0])
        # 余额支付,处理后类型float
        order_detail_balance_pay = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[1]/p[5]").text
        order_detail_balance_pay = turn_to_float(get_price(order_detail_balance_pay)[0])
        # 应付总额，处理后类型float
        order_detail_should_total = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[1]/p[6]").text
        print("总额", order_detail_should_total)
        all_price = get_price(order_detail_should_total)
        print("所有价格", all_price)
        order_detail_should_total = turn_to_float(all_price[0])
        # 总费用
        order_detail_should_total_all = turn_to_float(all_price[1])
        # 红包支付金额
        order_detail_should_total_red = turn_to_float(all_price[2])
        # 余额支付金额
        order_detail_should_total_balance = turn_to_float(all_price[3])
        # 应付总额2
        order_detail_should_total2 = turn_to_float(all_price[4])

        # 付款时间
        order_detail_pay_time = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[1]/p[8]").text
        order_detail_pay_time = process_order_infos(order_detail_pay_time)
        aa = {
            "order_detail_total_price": order_detail_total_price,
            "order_detail_red_packet": order_detail_red_packet,
            "order_detail_balance_pay": order_detail_balance_pay,
            "order_detail_should_total": order_detail_should_total,
            "order_detail_should_total_all": order_detail_should_total_all,
            "order_detail_should_total_red": order_detail_should_total_red,
            "order_detail_should_total_balance": order_detail_should_total_balance,
            "order_detail_should_total2": order_detail_should_total2,
            "order_detail_pay_time": order_detail_pay_time
        }
        print("订单详情", aa)
        # 收件人
        order_detail_receiver = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[2]/p[2]").text
        order_detail_receiver = process_order_infos(order_detail_receiver)
        # 收件地址
        order_detail_receive_address = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[2]/p[3]").text
        order_detail_receive_address = process_order_infos(order_detail_receive_address)
        # 手机号
        order_detail_receive_phone = self.driver.find_element_by_xpath(".//div[@class='caseComm']/div[2]/p[4]").text
        order_detail_receive_phone = process_order_infos(order_detail_receive_phone)
        bb = {
            "order_detail_receiver": order_detail_receiver,
            "order_detail_receive_address": order_detail_receive_address,
            "order_detail_receive_phone": order_detail_receive_phone
        }
        print("收件信息", bb)

        return {
            "goods_order_name": self.goods_name4,
            "goods_order_type": process_type(self.goods_type4),
            "goods_order_price": float(self.goods_price4),
            "goods_order_code": self.goods_code4,
            "goods_offical4": float(self.goods_offical4),
            "goods_order_total_price1": float(self.goods_total_price1),
            "goods_order_total_price2": float(self.goods_total_price2),
            "goods_order_total_price3": float(self.goods_total_price3),
            "goods_QR_price1": float(QR_price1),
            "goods_QR_price2": float(QR_price2),
            "goods_pay_price1": float(goods_pay_price1),
            "goods_pay_for_balance": float(goods_pay_for_balance),
            "goods_pay_price2": float(goods_pay_price2),
            "goods_pay_price3": float(goods_pay_price3),
            "get_usable_balance": float(get_usable_balance),
            "used_balance": float(used_balance),
            "pay_state": pay_state,
            "center_order_number": center_order_number,
            "center_pay_state": center_pay_state,
            "center_goods_name": center_goods_name,
            "center_goods_type": center_goods_type,
            "center_case_code": center_case_code,
            "center_case_price": float(center_case_price),

            "goods_trade_state": goods_trade_state,
            "goods_detail_name2": goods_detail_name2,

            "order_detail_pay_state": order_detail_pay_state,
            "order_detail_total_price": order_detail_total_price,
            "order_detail_red_packet": order_detail_red_packet,
            "order_detail_balance_pay": order_detail_balance_pay,
            "order_detail_should_total": order_detail_should_total,
            "order_detail_should_total_all": order_detail_should_total_all,
            "order_detail_should_total_red": order_detail_should_total_red,
            "order_detail_should_total_balance": order_detail_should_total_balance,
            "order_detail_should_total2": order_detail_should_total2,
            "order_detail_receiver": order_detail_receiver,
            "order_detail_receive_address": order_detail_receive_address,
            "order_detail_receive_phone": order_detail_receive_phone

        }

    # 案件中心
    # def case_centre(self):
    #     self.driver.find_element_by_xpath("")
