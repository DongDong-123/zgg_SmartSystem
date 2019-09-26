import unittest
import time
from HTMLTestRunner_PY3 import HTMLTestRunner
import os
from sendEmail import SendEmail


def begin():
    from test_trademark import TestListToDetail
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestListToDetail))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestListClue))

    timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    report_title = '商标交易用例执行报告'
    desc = '商标交易'
    report_file = './reports/{}_{}.html'.format(report_title, timetemp)
    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner(stream=report, title=report_title, description=desc, verbosity=2)
        runner.run(suite)

    file_path = os.path.join(os.getcwd(), report_file)
    email = SendEmail()
    email.send_mail(report_title, file_path)


# def send_clue():
#     from test_clue import TestListClue
#
#     suite = unittest.TestSuite()
#     suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestListClue))
#
#     timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
#     report_title = '提交报价用例执行报告'
#     desc = '提交报价'
#     report_file = 'reports/{}_{}.html'.format(report_title, timetemp)
#     with open(report_file, 'wb') as report:
#         runner = HTMLTestRunner(stream=report, title=report_title, description=desc, verbosity=2)
#         runner.run(suite)
#
#     file_path = os.path.join(os.getcwd(), report_file)
#     email = SendEmail()
#     email.send_mail(report_title, file_path)


# 删除
# def delete():
#     from delete_unpay_case import Execute
#     test = Execute()
#     num = test.get_code_num()
#     for i in range(num):
#         test.delete_order()
#     print("删除完毕，共删除{}个".format(num))
#
#
# def gai_zhang():
#     from gaizhang import Gaizhang
#     Gaizhang().gaizhang()


# def search():
#     from search_replay_invoice import SearchInvoice
#     SearchInvoice().search()


if __name__ == "__main__":
    begin()
    # send_clue()
    # delete()
    # gai_zhang()
    # search()
    print("over")