import time
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import math
import mysql
import mysql.connector as msql
from mysql.connector import Error
from webdriver_manager.chrome import ChromeDriverManager


# driver = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install())


def crawl_company(stock_name):
    first_page = driver.get('http://www.tsetmc.com/Loader.aspx?ParTree=15')
    time.sleep(3)
    second_page = driver.find_element_by_xpath('//*[@id="rainbow_global_1"]').click()
    time.sleep(3)
    third_page = driver.find_element_by_xpath('//*[@id="TseTab1Elm"]/div[3]/div[1]').click()
    time.sleep(3)
    stock_link = driver.find_element_by_link_text(stock_name)
    stock_link.click()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    stock_features = driver.find_element_by_xpath('//*[@id="tabs"]/div/ul/li[7]/a').click()
    time.sleep(5)


def crawl_history():
    stock_history = driver.find_element_by_xpath('//*[@id="tabs"]/div/ul/li[3]/a').click()
    time.sleep(5)


def scrape_features(stock_name):
    query1 = " CREATE DATABASE IF NOT EXISTS Stocks "
    query2 = " CREATE TABLE IF NOT EXISTS stockinfo(name varchar(255) PRIMARY key, companycode varchar(255),12code varchar(255)  ) "
    query3 = " CREATE TABLE IF NOT EXISTS stocks(name varchar(255) references stockinfo(name),date varchar(255), number int,volume float ,first float,high float ,low float ,value float ,last float ,close float, PRIMARY KEY (date ,name)) "
    try:
        conn = msql.connect(host='localhost', user='root', password='123123')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query1)
            print("Database is created")
    except Error as e:
        print("Error while connecting to MySQL", e)

    try:
        conn = msql.connect(host='localhost', database='Stocks', user='root', password='123123')
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            print('Creating table....')
            cursor.execute(query2)
            cursor.execute(query3)
            print("Tables are created....")

    except Error as e:
        print("Error while connecting to MySQL", e)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    dom = etree.HTML(str(soup))
    code_12_xpath = '//*[@id="PureData"]/div/div[2]/table/tbody/tr[1]/td[2]'
    company_code_xpath = '//*[@id="PureData"]/div/div[2]/table/tbody/tr[11]/td[2]'
    code_12 = driver.find_element_by_xpath(code_12_xpath).text
    company_code = driver.find_element_by_xpath(company_code_xpath).text

    condition_query2 = " SELECT * FROM Stocks.stockinfo WHERE name = %s "
    insertion_query2 = " INSERT INTO Stocks.stockinfo VALUES (%s, %s, %s)"

    try:
        conn = msql.connect(host='localhost', database='Stocks', user='root', password='123123')
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            cursor.execute(condition_query2, (stock_name,))
            count = cursor.rowcount
            if count == 0:
                cursor.execute(insertion_query2, (stock_name, company_code, code_12))
                print("inserted")
            conn.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)


def scrape(name, row_num):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    dom = etree.HTML(str(soup))
    # date
    date_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    date_xpath += str(row_num)
    date_xpath += ']/td[16]'
    dom.xpath(date_xpath)
    date = driver.find_element_by_xpath(date_xpath).text
    # number
    number_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    number_xpath += str(row_num)
    number_xpath += ']/td[15]'
    number = driver.find_element_by_xpath(number_xpath).text

    if ',' in number:
        number.replace(',', '')
    number = int(number)
    # volume
    volume_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    volume_xpath += str(row_num)
    volume_xpath += ']/td[14]/div'
    volume = driver.find_element_by_xpath(volume_xpath).text

    if ',' in volume:
        volume = volume.replace(',', '')

    if 'B' in volume:
        volume = volume.replace('B', '')
        volume = float(volume)
        volume = volume * math.pow(10, 9)
        volume = str(volume)

    if 'M' in volume:
        volume = volume.replace('M', '')
        volume = float(volume)
        volume = volume * math.pow(10, 6)
        volume = str(volume)

    volume = float(volume)

    # value

    value_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    value_xpath += str(row_num)
    value_xpath += ']/td[13]/div'
    value = driver.find_element_by_xpath(value_xpath).text

    if ',' in value:
        value = value.replace(',', '')

    if 'B' in value:
        value = value.replace('B', '')
        value = float(value)
        value = value * math.pow(10, 9)
        value = str(value)

    if 'M' in value:
        value = value.replace('M', '')
        value = float(value)
        value = value * math.pow(10, 6)
        value = str(value)

    value = float(value)

    # high

    high_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    high_xpath += str(row_num)
    high_xpath += ']/td[3]'
    high = driver.find_element_by_xpath(high_xpath).text

    if ',' in high:
        high = high.replace(',', '')

    high = int(high)
    # low
    low_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    low_xpath += str(row_num)
    low_xpath += ']/td[4]'
    low = driver.find_element_by_xpath(low_xpath).text

    if ',' in low:
        low = low.replace(',', '')

    low = int(low)

    # first

    first_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    first_xpath += str(row_num)
    first_xpath += ']/td[11]'
    first = driver.find_element_by_xpath(first_xpath).text

    if ',' in first:
        first = first.replace(',', '')

    first = int(first)

    # last

    last_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    last_xpath += str(row_num)
    last_xpath += ']/td[10]'
    last = driver.find_element_by_xpath(last_xpath).text

    if ',' in last:
        last = last.replace(',', '')

    last = int(last)

    # close

    close_xpath = '//*[@id="trade"]/div[2]/table/tbody/tr['
    close_xpath += str(row_num)
    close_xpath += ']/td[7]'
    close = driver.find_element_by_xpath(close_xpath).text

    if ',' in close:
        close = close.replace(',', '')

    close = int(close)

    data = {
        "Name": name,
        "Date": date,
        "Number": number,
        "Volume": volume,
        "First": first,
        "High": high,
        "Low": low,
        "Value": value,
        "Last": last,
        "Close": close
    }

    condition_query1 = " SELECT * FROM Stocks.stocks WHERE name = %s and date = %s "
    insertion_query1 = " INSERT INTO Stocks.stocks VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    data_f_s = pd.DataFrame(data, index=[0])
    print(data_f_s)
    try:
        conn = msql.connect(host='localhost', database='Stocks', user='root', password='123123')
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            cursor.execute(condition_query1, (name, date))
            count = cursor.rowcount
            if count == 0:
                cursor.execute(insertion_query1, (name, date, number, volume, first, high, low, value, last, close))
                print("inserted")
            else:
                quit()
            conn.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)

    return data_f_s


def scrape_rows(name):
    for x in range(2, 23):
        scrape(name, row_num=x)


def crawl_scrape_history(name, page_num, page_num_lim):
    scrape_rows(name)
    first_page = page_num
    last_page = page_num_lim
    page_xpath = '//*[@id="paging"]/div/a['
    page_xpath += str(page_num - 1)
    page_xpath += ']'
    driver.find_element_by_xpath(page_xpath).click()
    scrape_rows(name)
    first_page += 1
    while first_page < last_page:
        try:
            page_xpath = '//*[@id="paging"]/div/a['
            page_xpath += str(first_page)
            page_xpath += ']'
            driver.find_element_by_xpath(page_xpath).click()
            scrape_rows(name)
            first_page += 1
        except NoSuchElementException:
            print("no more element")
            break
    crawl_scrape_second(name, 3, 37)


def crawl_scrape_second(name, page_num, page_num_lim):
    first_page = page_num
    last_page = page_num_lim
    try:
        next_page_xpath = '//*[@id="paging"]/div/a['
        next_page_xpath += str(last_page)
        next_page_xpath += ']'
        time.sleep(1)
        driver.find_element_by_xpath(next_page_xpath).click()
        driver.find_element_by_xpath('//*[@id="paging"]/div/a[2]').click()
        time.sleep(1)
        scrape_rows(name)
        page_xpath = '//*[@id="paging"]/div/a['
        page_xpath += str(first_page)
        page_xpath += ']'
        driver.find_element_by_xpath(page_xpath).click()
        scrape_rows(name)
        first_page += 1
    except NoSuchElementException:
        print("no more element")

    while first_page < last_page:
        try:
            page_xpath = '//*[@id="paging"]/div/a['
            page_xpath += str(first_page)
            page_xpath += ']'
            driver.find_element_by_xpath(page_xpath).click()
            scrape_rows(name)
            first_page += 1
        except NoSuchElementException:
            print("no more element")
            break
    crawl_scrape_second(name, 3, 37)


def crawl_scrape(stock_name):
    crawl_company(stock_name)
    scrape_features(stock_name)
    crawl_history()
    crawl_scrape_history(stock_name, 3, 37)


def get_stocks(stock_name):

    query2 = " SELECT * FROM Stocks.stocks WHERE name = %s "
    try:
        conn = msql.connect(host='localhost', database='Stocks', user='root', password='123123')
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            cursor.execute(query2, (stock_name,))
            rows = cursor.fetchall()
            data = pd.DataFrame(rows, columns=['name', 'date', 'number', 'volume', 'first', 'high', 'low', 'value', 'last', 'close'])
            conn.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    return data


def get_excel(stock_name):

    query2 = " SELECT * FROM Stocks.stocks WHERE name = %s "
    try:
        conn = msql.connect(host='localhost', database='Stocks', user='root', password='123123')
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            cursor.execute(query2, (stock_name,))
            rows = cursor.fetchall()
            data = pd.DataFrame(rows, columns=['name', 'date', 'number', 'volume', 'first', 'high', 'low', 'value', 'last', 'close'])
            conn.commit()
            filename_needed = 'F:/Projects/Trader/TraderV001/Data/'
            filename_needed += stock_name
            filename_needed += '.csv'
            data.to_csv(filename_needed, index=False, header=True, encoding="utf-8")
    except Error as e:
        print("Error while connecting to MySQL", e)





