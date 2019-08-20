import unittest
import re
import time
from trademark_transaction import Trademark

goods_infos = Trademark().trademark_list()
goods_order = Trademark().trademark_order()


class TestListToDetail(unittest.TestCase):
    """此用例包含20个用例，测试商标交易列表页、详情页、下单页、交易管理页面商标信息是否正确"""
    goods_infos = Trademark().trademark_list()
    goods_order = Trademark().trademark_order()

    def setUp(self):
        print("begin the Test")
        self.goods_infos = goods_infos
        self.goods_order = goods_order

    # def tearDown(self):
    #     print("do something after test : clean up ")

    # 1
    def test_name_list_to_detail(self):
        """用例1：测试列表页名称与详情页名称是否一致"""
        self.assertEqual(self.goods_infos.get("goods_name"), self.goods_infos.get("goods_detail_name"))

    # 2
    def test_type_list_to_detail(self):
        """用例2：测试列表页大类与详情页大类是否一致"""
        self.assertEqual(self.goods_infos.get("goods_type"), self.goods_infos.get("goods_detail_type"))

    # 3
    def test_price_list_to_detail(self):
        """用例3：测试列表页价格与详情页价格是否一致"""
        self.assertEqual(self.goods_infos.get("goods_price"), self.goods_infos.get("goods_detail_price"))

    # 4
    def test_name_detail_to_order(self):
        """用例4：测试详情页名称与订单页名称是否一致"""
        self.assertEqual(self.goods_infos.get("goods_detail_name"), self.goods_order.get("goods_order_name"))

    # 5
    def test_type_detail_to_order(self):
        """用例5：测试详情页大类与订单页大类是否一致"""
        self.assertEqual(self.goods_infos.get("goods_detail_type"), self.goods_order.get("goods_order_type"))

    # 6
    def test_price_detail_to_order(self):
        """用例6：测试详情页价格与订单页价格是否一致"""
        self.assertEqual(self.goods_infos.get("goods_detail_price"), self.goods_order.get("goods_order_price"))

    # 7
    def test_case_number(self):
        """用例7：测试案件号是格式是否正确"""
        patten = "GG\d{6,10}TM-JY"
        res = re.search(patten, self.goods_order.get("goods_order_code"))
        self.assertNotEqual(res, None)

    # 8
    def test_offical_price(self):
        """用例8：测试官费是否正确"""
        self.assertEqual(self.goods_order.get("goods_offical4"), 450.00)

    # 9
    def test_total_price(self):
        """用例9：测试总价格是否正确"""
        self.assertEqual(self.goods_order.get("goods_order_total_price1"),
                         self.goods_order.get("goods_order_price") + 450.00)

    # 10
    def test_total_price_is_same1(self):
        """用例10：测试第一、第二个位置的总价格是否一致"""
        self.assertEqual(self.goods_order.get("goods_order_total_price1"),
                         self.goods_order.get("goods_order_total_price2"))

    # 11
    def test_total_price_is_same2(self):
        """用例11：测试第一、第三个位置的总价格是否一致"""
        self.assertEqual(self.goods_order.get("goods_order_total_price1"),
                         self.goods_order.get("goods_order_total_price3"))

    # 支付页面测试
    # 12
    def test_pay_price(self):
        """用例12：测试总费用是否等于余额支付加应付总额"""
        self.assertEqual(self.goods_order.get("goods_pay_price1"),
            self.goods_order.get("goods_pay_price2") - self.goods_order.get("goods_pay_for_balance"))

    # 13
    def test_pay_total(self):
        """用例13：测试上下应付总额是否相同"""
        self.assertEqual(self.goods_order.get("goods_pay_price2"), self.goods_order.get("goods_pay_price3"))

    # 14
    def test_balance_pay(self):
        """用例14：测试已使用余额与余额支付金额是否相等"""
        self.assertEqual(-self.goods_order.get("goods_pay_for_balance"), self.goods_order.get("used_balance"))

    # 15
    def test_total_to_QR_price(self):
        """用例15：测试总金额与二维码页面支付金额是否相等"""
        self.assertEqual(self.goods_order.get("goods_pay_price3"), self.goods_order.get("goods_QR_price2"))

    # 16
    def test_QR_price(self):
        """用例16：测试二维码页面上下价格是否相等，二维码价格为0，表示未使用二维码支付"""
        self.assertEqual(self.goods_order.get("goods_QR_price1"), self.goods_order.get("goods_QR_price2"))

    # 交易管理列表
    # 17
    def test_caseinfo_for_name(self):
        """用例17：测试商标名称是否与列表页一致"""
        self.assertEqual(self.goods_order.get("center_goods_name"), self.goods_infos.get("goods_name"))

    # 18
    def test_caseinfo_for_type(self):
        """用例18：测试商品分类是否是商标"""
        self.assertEqual(self.goods_order.get("center_goods_type"), "商标")

    # 19
    def test_caseinfo_for_case_number(self):
        """用例19：测试案件中心案件号是否与下单页案件号一致"""
        self.assertEqual(self.goods_order.get("center_case_code"), self.goods_order.get("goods_order_code"))

    # 20
    def test_caseinfo_for_case_price(self):
        """用例20：测试案件中心案件金额是否与下单页总费用一致"""
        self.assertEqual(self.goods_order.get("center_case_price"), self.goods_order.get("goods_pay_price1"))

    # 案件管理-商标详情
    # 20
    def test_caseinfo_for_case_state(self):
        """用例20：测试商标详情页商标状态是否为交易中……"""
        self.assertEqual(self.goods_order.get("goods_trade_state"), "商品交易中...")

    # 20
    def test_caseinfo_for_case_name(self):
        """用例20：测试案件中心案件商标名称是否与商标详情页一致"""
        self.assertEqual(self.goods_order.get("goods_detail_name2"), self.goods_order.get("center_goods_name"))

    # 订单详情
    # 20
    def test_order_detail_pay_state(self):
        """用例20：测试订单详情页支付方式是否与支付页选择一致"""
        self.assertEqual(self.goods_order.get("order_detail_pay_state"), self.goods_order.get("pay_state"))

    # 20
    def test_order_detail_total_price(self):
        """用例20：测试订单详情总费用是否与下单页总费用一致"""
        self.assertEqual(self.goods_order.get("order_detail_total_price"), self.goods_order.get("goods_pay_price3"))

    # 20
    def test_order_detail_used_balance(self):
        """用例20：测试订单详情页余额支付金额是否与支付页余额支付金额一致"""
        self.assertEqual(self.goods_order.get("order_detail_balance_pay"), self.goods_order.get("used_balance"))

    def test_order_detail_should_pay(self):
        """用例20：测试订单详情页应付总额是否与支付页应付总额一致"""
        self.assertEqual(self.goods_order.get("order_detail_should_total"), self.goods_order.get("goods_pay_price3"))

    def test_order_detail_total_pay(self):
        """用例20：测试订单详情页总费用是否与应付总额中总费用一致"""
        self.assertEqual(self.goods_order.get(
            "order_detail_total_price"), self.goods_order.get("order_detail_should_total_all"))

    def test_order_detail_shoud_total_pay(self):
        """用例20：测试订单详情页应付总额与总费用-红包-余额支付，计算出的金额是否相同"""
        self.assertEqual(self.goods_order.get("order_detail_should_total2"), self.goods_order.get("order_detail_should_total"))

    def test_order_detail_pay_time(self):
        """用例20：测试订单详情页余额支付金额是否与支付页余额支付金额一致"""
        self.assertEqual(self.goods_order.get("order_detail_balance_pay"), self.goods_order.get("used_balance"))

