import unittest
from send_clue import Send_Clue, Trademark

goods_list_info = Send_Clue().test_list_page()
goods_detail_info = Trademark().trademark_list()

"""
{
            "goods_name": goods_name,
            "goods_type": goods_type,
            "goods_suit": goods_suit,
            "goods_deadline": goods_deadline,
            "goods_price": goods_price
        }
"""
"""
{
            "goods_name": self.goods_name,
            "goods_type": self.goods_type,
            "goods_price": float(self.goods_price),
            "goods_detail_name": self.goods_detail_name,
            "goods_detail_type": self.goods_detail_type,
            "goods_detail_price": float(self.goods_detail_price)
        }
"""


class TestListClue(unittest.TestCase):
    def setUp(self):
        self.goods_list_info = goods_list_info
        self.goods_detail_info = goods_detail_info

    def test_name_page_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("goods_name"),self.goods_detail_info.get("goods_name"))

    def test_type_page_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("goods_type"),self.goods_detail_info.get("goods_type"))

    def test_price_page_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("goods_price"),self.goods_detail_info.get("goods_price"))

    def test_deadline_page_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("goods_deadline"),self.goods_detail_info.get("goods_deadline"))

    def test_send_result_list(self):
        """测试是否发送成功"""
        self.assertEqual(self.goods_list_info.get("send_result"), True)


