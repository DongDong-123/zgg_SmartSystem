import unittest
import re
import time
from HTMLTestRunner_PY3 import HTMLTestRunner
import os

from sendEmail import SendEmail
from test_trademark import TestListToDetail


def begin():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestListToDetail))

    timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    report_title = '商标交易用例执行报告'
    desc = '商标交易'
    report_file = 'reports/Report_{}.html'.format(timetemp)
    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner(stream=report, title=report_title, description=desc, verbosity=2)
        runner.run(suite)

    file_path = os.path.join(os.getcwd(), report_file)
    email = SendEmail()
    email.send_mail(report_title, file_path)


if __name__ == "__main__":
    begin()
