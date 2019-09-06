import re

# 处理价格
def process_price(price):
    if not price:
        return 0
    if isinstance(price, str):
        if "面议" in price:
            return 0
        elif '￥' or '¥' or '元' in price:
            patt = "['￥','¥','元']"
            return re.sub(patt, "", price)
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
    else:
        raise ValueError


def check_rasult(driver):
    result = driver.find_elements_by_xpath("(.//div[@class='comm']/p)")[0]
    print(result)
    # result = result[0]
    result = result.text
    print("result", result, type(result))

    if "您的查询资料已提交" in result:
        response = "True"
    else:
        response = "False"
    return response

# 处理分类，只取分类号
def process_type(elem):
    patten = "(\d+)"
    result = re.search(patten, elem)
    if result:
        return result.group()
    else:
        return None

# 处理支付方式
def process_order_infos(elem):
    patten = ".*?：(.*)"
    result = re.search(patten, elem)
    if result:
        return result.group(1)
    else:
        return None

# 提取价格
def get_price(elem):
    patten = ".*?(\d+\.\d+).*?"
    result = re.findall(patten, elem)
    print(result)
    if result:
        return result

def turn_to_float(elem):
    if elem:
        return float(elem)



if __name__ == "__main__":
    # elem = "应付总额：¥0.0【23450.00(总费用) - 0.00(红包) - 23450.00(余额)=0.00】"
    # elem = "总费用：¥"
    # print(get_price(elem))
    strs = '付款方式：支付宝'
    aa = process_order_infos(strs)
    print(aa)
