import unittest
import re
import time
from trademark_transaction import Trademark

goods_list, goods_detail = Trademark().trademark_list()
goods_order, QR_price, goods_pay, goods_case = Trademark().trademark_order()


class TestListToDetail(unittest.TestCase):
    """此用例包含20个用例，测试商标交易列表页、详情页、下单页、交易管理页面商标信息是否正确"""

    def setUp(self):
        print("begin the Test")
        self.goods_list, self.goods_detail = goods_list, goods_detail
        self.goods_order, self.QR_price, self.goods_pay, self.goods_case = goods_order, QR_price, goods_pay, goods_case

    # def tearDown(self):
    #     print("do something after test : clean up ")

    # 1
    def test_name_list_to_detail(self):
        """用例1：测试列表页名称与详情页名称是否一致"""
        self.assertEqual(self.goods_list[0], self.goods_detail[0])

    # 2
    def test_type_list_to_detail(self):
        """用例2：测试列表页大类与详情页大类是否一致"""
        patten = "(\d+)"
        type1 = re.search(patten, self.goods_list[1])
        type2 = re.search(patten, self.goods_detail[1])
        self.assertEqual(type2.group(), type1.group())

    # 3
    def test_price_list_to_detail(self):
        """用例3：测试列表页价格与详情页价格是否一致"""
        self.assertEqual(self.goods_list[2], self.goods_detail[2])

    # 4
    def test_name_detail_to_order(self):
        """用例4：测试详情页名称与订单页名称是否一致"""
        self.assertEqual(self.goods_detail[0], self.goods_order[0])

    # 5
    def test_type_detail_to_order(self):
        """用例5：测试详情页大类与订单页大类是否一致"""
        patten = "(\d+)"
        type1 = re.search(patten, self.goods_detail[1])
        type2 = re.search(patten, self.goods_order[1])
        self.assertEqual(type2.group(), type1.group())

    # 6
    def test_price_detail_to_order(self):
        """用例6：测试详情页价格与订单页价格是否一致"""
        self.assertEqual(self.goods_detail[2], self.goods_order[2])

    # 7
    def test_case_number(self):
        """用例7：测试案件号是格式是否正确"""
        patten = "GG\d{6,10}TM-JY"
        res = re.search(patten, self.goods_order[3])
        self.assertNotEqual(res, None)

    # 8
    def test_offical_price(self):
        """用例8：测试官费是否正确"""
        self.assertEqual(self.goods_order[4], "450")

    # 9
    def test_total_price(self):
        """用例9：测试总价格是否正确"""
        self.assertEqual(float(self.goods_order[5]), float(self.goods_order[2]) + 450.00)

    # 10
    def test_total_price_is_same1(self):
        """用例10：测试第一、第二个位置的总价格是否一致"""
        self.assertEqual(self.goods_order[5], self.goods_order[6])

    # 11
    def test_total_price_is_same2(self):
        """用例11：测试第一、第三个位置的总价格是否一致"""
        self.assertEqual(self.goods_order[5], self.goods_order[7])

    # 支付页面测试
    # 12
    def test_pay_price(self):
        """用例12：测试总费用是否等于余额支付加应付总额"""
        self.assertEqual(float(self.goods_pay[0]), float(self.goods_pay[2]) - float(self.goods_pay[1]))

    # 13
    def test_pay_total(self):
        """用例13：测试上下应付总额是否相同"""
        self.assertEqual(float(self.goods_pay[2]), float(self.goods_pay[3]))

    # 14
    def test_balance_pay(self):
        """用例14：测试已使用余额与余额支付金额是否相等"""
        self.assertEqual(-float(self.goods_pay[1]), float(self.goods_pay[5]))

    # 15
    def test_total_to_QR_price(self):
        """用例15：测试总金额与二维码页面支付金额是否相等"""
        self.assertEqual(float(self.goods_pay[3]), float(self.QR_price[1]))

    # 16
    def test_QR_price(self):
        """用例16：测试二维码页面上下价格是否相等"""
        self.assertEqual(float(self.QR_price[0]), float(self.QR_price[1]))

    # 交易管理列表
    # 17
    def test_caseinfo_for_name(self):
        """用例17：测试商标名称是否与列表页一致"""
        self.assertEqual(self.goods_case[2], self.goods_list[0])

    # 18
    def test_caseinfo_for_type(self):
        """用例18：测试商品分类是否是商标"""
        self.assertEqual(self.goods_case[3], "商标")

    # 19
    def test_caseinfo_for_case_number(self):
        """用例19：测试案件号是否与下单页一致"""
        self.assertEqual(self.goods_case[4], self.goods_order[3])

    # 20
    def test_caseinfo_for_case_price(self):
        """用例20：测试案件号是否与下单页一致"""
        self.assertEqual(self.goods_case[5], self.goods_pay[3])
