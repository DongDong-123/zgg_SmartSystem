from selenium import webdriver
from readConfig import ReadConfig
import unittest
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.action_chains import ActionChains
import re
from front_login import *
import time
from Common_func import process_price, check_rasult, process_type


num = random.randint(1, 20)  # 随机选择一个商标


driver = webdriver.Chrome()


class Send_Clue:
    def __init__(self):
        self.driver = driver
        self.timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    def test_list_page(self):
        self.driver.maximize_window()

        list_url = "https://market.zgg.com/market/productlist.html"
        self.driver.get(list_url)

        # num = random.randint(1, 20)  # 随机选择一个商标
        print("num", num)
        list_goods_name = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/p".format(num)).text
        list_goods_type = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/h2".format(num)).text
        list_goods_type = process_type(list_goods_type)
        list_goods_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a/span".format(num)).text
        list_goods_price = process_price(list_goods_price)
        # 打印参数
        print("aa", [list_goods_name, list_goods_type, list_goods_price])

        goods_pic = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/a".format(num))
        ActionChains(self.driver).move_to_element(goods_pic).perform()
        self.say_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-pro-item']/ul/li[{}]/div/div[1]".format(num)).click()
        # 弹框信息
        time.sleep(1)
        frame_goods_name = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[1]/span[2]").text

        frame_goods_type = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[2]/span[2]").text
        frame_goods_type = process_type(frame_goods_type)

        frame_goods_suit = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[3]/span[2]").text

        frame_goods_deadline = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[4]/span[2]").text

        frame_goods_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-offer-contart']/div[@class='offerInformation']/div[5]/span[2]").text
        frame_goods_price = process_price(frame_goods_price)

        print("bb",
            {
            "frame_goods_name": frame_goods_name,
            "frame_goods_type": frame_goods_type,
            "frame_goods_suit": frame_goods_suit,
            "frame_goods_deadline": frame_goods_deadline,
            "frame_goods_price": frame_goods_price,
             })

        your_name = "张三"
        your_phone = "16619923387"
        your_price = '2000'
        self.driver.find_element_by_xpath(".//div[@class='speical-box']/div[2]/input").send_keys(your_phone)
        self.driver.find_element_by_xpath(".//div[@class='speical-box']/div[1]/input").send_keys(your_name)
        self.driver.find_element_by_xpath(".//div[@class='speical-box']/div[3]/input").send_keys(your_price)
        time.sleep(1)
        # 提交
        self.driver.find_element_by_xpath(".//div[@class='offer-sure']/a").click()
        result = check_rasult(self.driver)
        self.driver.save_screenshot("screen\发送结果{}.png".format(self.timetemp))
        time.sleep(0.5)
        # self.driver.find_element_by_xpath(".//div[@class='input-btn']/a").click()
        self.driver.refresh()
        time.sleep(1)
        self.driver.find_element_by_xpath(".//div[@class='tm-mark-pro-item']/ul/li[{}]/a".format(num)).click()

        # 进入详情页
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        detail_title = self.driver.title
        print(detail_title)
        goods_detail_name = self.driver.find_element_by_xpath(".//div[@class='title']/h2").text
        goods_detail_type = self.driver.find_element_by_xpath(
            ".//table[@class='tm-mark-detai-table']/tbody/tr[1]/td[2]").text
        goods_detail_type = process_type(goods_detail_type)
        # 新增===========
        goods_detail_deadline = self.driver.find_element_by_xpath(
            ".//table[@class='tm-mark-detai-table']/tbody/tr[4]/td[2]").text
        # ===============
        goods_detail_price = self.driver.find_element_by_xpath(
            ".//div[@class='tm-mark-detail-money']/div/span/em").text
        print([goods_detail_name, goods_detail_type, goods_detail_price])
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

        print([goods_detail_deadline, name_for_Product_details, type_for_Product_details, deadline_for_Product_details])
        self.driver.quit()
        cc = {
            "goods_detail_name": goods_detail_name,
            "goods_detail_type": goods_detail_type,
            "goods_detail_price": float(goods_detail_price),
            "goods_deadline": goods_detail_deadline

        }
        print("cc", cc)
        return {
            "list_goods_name": list_goods_name,
            "list_goods_type": list_goods_type,
            "list_goods_price": float(list_goods_price),

            "frame_goods_name": frame_goods_name,
            "frame_goods_type": frame_goods_type,
            "frame_goods_suit": frame_goods_suit,
            "frame_goods_deadline": frame_goods_deadline,
            "frame_goods_price": float(frame_goods_price),
            "send_result": result,
            "goods_detail_name": goods_detail_name,
            "goods_detail_type": goods_detail_type,
            "goods_detail_price": float(goods_detail_price),
            "goods_detail_deadline": goods_detail_deadline

        }
