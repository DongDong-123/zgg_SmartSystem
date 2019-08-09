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


detail_url = None


# 处理价格
def process_price(price):
    if isinstance(price, str):
        if "￥" in price:
            return price.replace("￥", "")
        elif "面议" in price:
            return price
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

    def setUp(self):
        print("this setupclass() method only called once")
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
        # self.driver.quit()
        return [self.goods_name, self.goods_type, self.goods_price], [self.goods_name2, self.goods_type2, self.goods_price2]

    def detail(self):
        self.driver = front_login(ReadConfig().get_user(), ReadConfig().get_password())
        self.driver.get(detail_url)
        print(self.driver.current_url)
        print(self.driver.title)
        # self.goods_name3 = self.driver.find_element_by_xpath(".//div[@class='title']/h2").text
        # self.goods_type3 = self.driver.find_element_by_xpath(".//table[@class='tm-mark-detai-table']/tbody/tr[1]/td[2]").text
        # self.goods_price3 = self.driver.find_element_by_xpath(".//div[@class='tm-mark-detail-money']/div/span/em").text
        # print([self.goods_name3, self.goods_type3, self.goods_price3])

        self.driver.find_element_by_xpath(".//div[@id='productId']/a[1]").click()
        time.sleep(1)

        self.goods_type4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[1]").text
        self.goods_name4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[2]").text
        self.goods_code4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[3]").text
        self.goods_price4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[4]").text
        self.goods_offical4 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[5]").text
        self.goods_total_price1 = self.driver.find_element_by_xpath(".//tbody/tr[@class='tr-comm']/td[6]").text

        self.goods_total_price2 = self.driver.find_element_by_xpath(".//div[@class='fwfBox']//div/em").text
        self.goods_total_price2 = process_price(self.goods_total_price2)

        self.goods_total_price3 = self.driver.find_element_by_xpath(".//div[@class='totalPrice']//div/b").text
        self.goods_total_price3 = process_price(self.goods_total_price3)

        print(self.goods_type4, self.goods_name4, self.goods_code4, self.goods_price4, self.goods_offical4,
              self.goods_total_price1, self.goods_total_price2, self.goods_total_price3)
# [self.goods_name3, self.goods_type3, self.goods_price3], \
        return [self.goods_name4, self.goods_type4, self.goods_price4, self.goods_code4, self.goods_offical4,
              self.goods_total_price1, self.goods_total_price2, self.goods_total_price3]


goods_list, goods_detail = Trademark().setUp()
goods_order = Trademark().detail()


class TestListToDetail(unittest.TestCase):
    # 继承自unittest.TestCase
    # 重写TestCase的setUp()、tearDown()方法：在每个测试方法执行前以及执行后各执行一次
    def setUp(self):
        print("this setupclass() method only called once")
        self.goods_list = goods_list
        self.goods_detail = goods_detail
        self.goods_order = goods_order

    def tearDown(self):
        print("do something after test : clean up ")

    def test_name_list_to_detail(self):
        self.assertEqual(self.goods_list[0], self.goods_detail[0])

    def test_type_list_to_detail(self):
        patten = "(\d+)"
        type1 = re.search(patten, self.goods_list[1])
        type2 = re.search(patten, self.goods_detail[1])
        # print(type2.group(), type1.group())
        self.assertEqual(type2.group(), type1.group())

    def test_price_list_to_detail(self):
        self.assertEqual(self.goods_list[2], self.goods_detail[2])

    def test_name_detail_to_order(self):
        self.assertEqual(self.goods_detail[0], self.goods_order[0])

    def test_type_detail_to_order(self):
        patten = "(\d+)"
        type1 = re.search(patten, self.goods_detail[1])
        type2 = re.search(patten, self.goods_order[1])
        # print(type2.group(), type1.group())
        self.assertEqual(type2.group(), type1.group())

    def test_price_detail_to_order(self):
        self.assertEqual(self.goods_detail[2], self.goods_order[2])

    def test_case_number(self):
        patten = "GG\d{6,10}TM-JY"
        res = re.search(patten, self.goods_order[3])
        self.assertNotEqual(res, None)

    def test_offical_price(self):
        self.assertEqual(self.goods_order[4], "450")

    def test_total_price(self):
        self.assertEqual(self.goods_order[5], self.goods_order[6])
        self.assertEqual(self.goods_order[5], self.goods_order[7])


print("name:", __name__)

if __name__ != "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestListToDetail))

    timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    report_title = '商标交易用例执行报告'
    desc = '商标交易'
    report_file = 'reports/ExampleReport_{}.html'.format(timetemp)

    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner(stream=report, title=report_title, description=desc, verbosity=2)
        runner.run(suite)
