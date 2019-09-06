from selenium import webdriver
from readConfig import ReadConfig
import unittest
from selenium.webdriver.chrome.options import Options
import random
import re
import time
from Common_func import *
from login_for_gaizhang import *
from selenium.webdriver.common.action_chains import ActionChains

# num = random.randint(1, 20)  # 随机选择一个商标
# driver = webdriver.Chrome()
# driver.maximize_window()


# url = "https://manage.zgg.com/com/bg/contract_list.html?step=4&seal_state=0&types=1,3"



class Gaizhang:
    def __init__(self):
        self.num = 1
        self.USER = ReadConfig().get_user()
        self.PASSWORD = ReadConfig().get_password()
        self.driver = front_login(self.USER, self.PASSWORD)
        self.page = 1
        self.url = "https://manage.zgg.com/com/bg/contract_list.html?step=4&types=1%2C3&field=TM&state=&code=&htcode=&employee=&seal_state=0&template_state=&user=&companyname=&fs=0&pay_state=&ordercode=&apply_st=&apply_et=2019-08-29&pay_st=&pay_et=&file_st=&file_et=&min_amount=&max_amount=&p={}".format(self.page)
        # self.url = "https://manage.zgg.com/com/bg/contract_list.html?step=4&types=1%2C3&field=CR&state=&code=&htcode=&employee=&seal_state=0&template_state=&user=&companyname=&fs=0&pay_state=&ordercode=&apply_st=&apply_et=2019-08-29&pay_st=&pay_et=&file_st=&file_et=&min_amount=&max_amount=&p={}".format(self.page)
        self.tt = 0
        self.screen_num = 1
    def gaizhang(self):

        # 未支付
        # url = "https://manage.zgg.com/com/bg/contract_list.html?step=4&types=1%2C3&field=TM&state=&code=&htcode=&employee=&seal_state=0&template_state=&user=&companyname=&fs=0&pay_state=1&apply_st=&apply_et=2019-08-29&pay_st=&pay_et=&file_st=&file_et=&min_amount=&max_amount="
        # 不限制支付方式
        self.driver.get(self.url)
        self.driver.save_screenshot("screen/hetong_{}.png".format(self.screen_num))
        self.screen_num += 1
        # driver.quit()

        for n in range(1, 1000):
            self.opeart()
            self.tt += 1
            print("--------------------------------{}----------------------".format(self.tt))

    def opeart(self):
        try:
            self.change_page()
            type_choice = self.driver.find_element_by_xpath(".//tr[@data='{}']/td[1]".format(self.num)).text
        except Exception as e:
            print("查找元素错误", e)
            return
        print(type_choice)
        is_opeart = choice_gaizhang(type_choice)
        if is_opeart:
            print("符合盖章条件")
            # windows = self.driver.window_handles
            # print("1", windows)
            link_text1 = self.driver.find_element_by_xpath("//tr[@data='{}']/td[5]/a[2]".format(self.num)).text
            link_text2 = self.driver.find_element_by_xpath("//tr[@data='{}']/td[5]/a[3]".format(self.num)).text
            print("按钮", link_text1, link_text2)
            if link_text1 == "合同盖章":
                print("1:", link_text1)
                try:
                    self.driver.find_element_by_xpath("//tr[@data='{}']/td[5]/a[2]".format(self.num)).click()
                except Exception as e:
                    print("点击合同盖章错误：", e)
                    self.driver.refresh()
            elif link_text2 == "合同盖章":
                print("2:", link_text2)

                self.driver.find_element_by_xpath("//tr[@data='{}']/td[5]/a[3]".format(self.num)).click()
            else:
                self.num += 1
                print("不是合同盖章按钮")
                self.write_log(type_choice, "button_error")
                self.driver.refresh()
                return

            time.sleep(1)
            self.driver.save_screenshot("screen/1.png")
            time.sleep(1)
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
                time.sleep(1)
                # texts = self.driver.find_element_by_xpath(".//div[@class='remove_div']/div[@class='maskbtnbx']").text
                check_res = self.driver.find_element_by_xpath(".//div[@class='seal_div']/div[@class='masklist']/p").text
                # print(texts)
                print(check_res)
            except Exception as e:
                check_res = None
                print("e", e)
                self.driver.refresh()
                self.num += 1
                return
            if check_res == "是否确认该合同为已盖章?":
                self.driver.find_element_by_xpath(".//div[@class='seal_div']/div[@class='maskbtnbx']/div").click()
                time.sleep(1)
                aler = self.driver.switch_to.alert
                print(aler.text)
                aler.accept()
                self.write_log(type_choice, "success")

            else:
                print("有问题")
                self.write_log(type_choice, "problem")

        else:
            print("不符合盖章条件："+"\n")
            self.num += 1
            self.write_log(type_choice, "no_gaizhang")




    def write_log(self, elem, name):
        if not isinstance(elem, str):
            elem = str(elem)

        with open("{}.log".format(name), "+a", encoding="utf-8") as f:
            f.write(elem + "\n")

    def change_page(self):
        print("num", self.num)
        if self.num > 20:
            print("page", self.page)
            self.page += 1
            self.url = "https://manage.zgg.com/com/bg/contract_list.html?step=4&types=1%2C3&field=TM&state=&code=&htcode=&employee=&seal_state=0&template_state=&user=&companyname=&fs=0&pay_state=&ordercode=&apply_st=&apply_et=2019-08-29&pay_st=&pay_et=&file_st=&file_et=&min_amount=&max_amount="
            # self.url = "https://manage.zgg.com/com/bg/contract_list.html?step=4&types=1%2C3&field=CR&state=&code=&htcode=&employee=&seal_state=0&template_state=&user=&companyname=&fs=0&pay_state=&ordercode=&apply_st=&apply_et=2019-08-29&pay_st=&pay_et=&file_st=&file_et=&min_amount=&max_amount="
            self.write_log(self.page, "page")
            self.num = 1
            self.driver.get(self.url)


def choice_gaizhang(elem):
    patten = "半纸质版"
    patten2 = "未盖章"
    res_type = re.search(patten, elem)
    if res_type:
        res_status = re.search(patten2, elem)
        if res_status:
            return True
    else:
        return False

