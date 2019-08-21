import unittest
from send_clue import Send_Clue

goods_list_info = Send_Clue().test_list_page()


class TestListClue(unittest.TestCase):
    def setUp(self):
        self.goods_list_info = goods_list_info
        # self.goods_detail_info = goods_detail_info

    def test_name_frame_list(self):
        """测试列表页提交报价中商标名称和列表页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_name"), self.goods_list_info.get("list_goods_name"))

    def test_type_frame_list(self):
        """测试列表页提交报价中商标名称和列表页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_type"), self.goods_list_info.get("list_goods_type"))

    def test_price_frame_list(self):
        """测试列表页提交报价中商标名称和列表页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_price"), self.goods_list_info.get("list_goods_price"))

    def test_deadline_frame_list(self):
        """测试列表页提交报价中有效期限和列表页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_deadline"),
                         self.goods_list_info.get("goods_detail_deadline"))

    def test_send_result_list(self):
        """测试提交报价是否发送成功"""
        self.assertEqual(self.goods_list_info.get("send_result"), True)

    def test_name_frame_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_name"), self.goods_list_info.get("goods_detail_name"))

    def test_type_frame_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_type"), self.goods_list_info.get("goods_detail_type"))

    def test_price_frame_detail(self):
        """测试列表页提交报价中商标名称和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_price"), self.goods_list_info.get("goods_detail_price"))

    def test_deadline_frame_detail(self):
        """测试列表页提交报价中有效期限和详情页中是否一致"""
        self.assertEqual(self.goods_list_info.get("frame_goods_deadline"),
                         self.goods_list_info.get("goods_detail_deadline"))
