from selenium import webdriver
from readConfig import ReadConfig
import unittest
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.action_chains import ActionChains
import re
from front_login import *
import time
from Common_func import process_price, check_rasult


num = random.randint(1, 20)  # 随机选择一个商标


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

        # num = random.randint(1, 20)  # 随机选择一个商标
        # num = 5
        # 获取商标名称、大类、价格
        self.goods_name = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/p".format(num)).text
        self.goods_type = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/h2".format(num)).text
        self.goods_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/span".format(num)).text
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
        self.goods_detail_type = self.driver.find_element_by_xpath(
            ".//table[@class='tm-mark-detai-table']/tbody/tr[1]/td[2]").text
        # 新增===========
        self.deadline = self.driver.find_element_by_xpath(
            ".//table[@class='tm-mark-detai-table']/tbody/tr[4]/td[2]").text
        # ===============
        self.goods_detail_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-detail-money']/div/span/em").text
        print([self.goods_detail_name, self.goods_detail_type, self.goods_detail_price])
        global detail_url
        detail_url = self.driver.current_url
        print("打印", detail_url)

        # 新增信息
        name_for_Product_details = self.driver.find_element_by_xpath(
            ".//table[@class='tm-detail-pro-table']/tbody/tr[1]/td[2]").text

        type_for_Product_details = self.driver.find_element_by_xpath(
            ".//table[@class='tm-detail-pro-table']/tbody/tr[2]/td[2]").text

        deadline_for_Product_details = self.driver.find_element_by_xpath(
            ".//table[@class='tm-detail-pro-table']/tbody/tr[5]/td[4]").text

        print([self.deadline, name_for_Product_details, type_for_Product_details, deadline_for_Product_details])
        self.driver.quit()
        return {
            "goods_name": self.goods_name,
            "goods_type": self.goods_type,
            "goods_price": float(self.goods_price),
            "goods_detail_name": self.goods_detail_name,
            "goods_detail_type": self.goods_detail_type,
            "goods_detail_price": float(self.goods_detail_price),
            "goods_deadline": self.deadline
        }


class Send_Clue:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_list_page(self):
        list_url = "https://market.zgg.com/market/productlist.html"
        self.driver.get(list_url)

        # num = random.randint(1, 20)  # 随机选择一个商标

        goods_pic = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a".format(num))
        ActionChains(self.driver).move_to_element(goods_pic).perform()
        self.say_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/div/div[1]".format(num)).click()

        goods_name = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[1]/span[2]").text

        goods_type = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[2]/span[2]").text

        goods_suit = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[3]/span[2]").text

        goods_deadline = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[4]/span[2]").text

        goods_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[5]/span[2]").text
        goods_price = process_price(goods_price)

        print(
            {"goods_name": goods_name,
             "goods_type": goods_type,
             "goods_suit": goods_suit,
             "goods_deadline": goods_deadline,
             "goods_price": goods_price
             })

        your_name = "张三"
        self.driver.find_element_by_xpath(".//div[@class='speical-box']/div[1]/input").send_keys(your_name)
        your_phone = "16619923387"
        self.driver.find_element_by_xpath(".//div[@class='speical-box']/div[2]/input").send_keys(your_phone)
        your_price = 2000
        self.driver.find_element_by_xpath(".//div[@class='speical-box']/div[2]/input").send_keys(your_price)
        time.sleep(1)
        # 提交
        self.driver.find_element_by_xpath(".//div[@class='offer-sure']/a").click()
        result = check_rasult(self.driver)

        return {
            "goods_name": goods_name,
            "goods_type": goods_type,
            "goods_suit": goods_suit,
            "goods_deadline": goods_deadline,
            "goods_price": goods_price,
            "send_result": result
        }
