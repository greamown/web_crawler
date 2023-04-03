import logging, sys, time
from common import logger, init_db, thread_pool, insert_table, db_to_csv, check_data_status, CSV_PATH
from argparse import ArgumentParser, SUPPRESS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures

INPUTKEY = '//input[@class="l-header__siteSearchInput"]'
BLOCKCLASS = '//dl[@class="col3f"]'
TEXTCLASS = 'prod_name'
PRICECLASS = 'value'
HREF = '//a[@href]'

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-u', '--url', required=True, help = "The URL of the crawler.")
    args.add_argument('-v', '--value', required=True, help = "The value of search.")
    return parser

def batch_insert(data):
    table_name = "gpu"
    keys = "ITEM, PRICE"
    values = "\'{}\', {}".format(data["item"], data["price"])
    content = "ITEM=\'{}\' AND PRICE={}".format(data["item"], data["price"])
    status = check_data_status(table_name, content)
    if not status:
        logging.info("Append data to database...")
        insert_table(table_name, keys, values)
    result = "result"
    future = concurrent.futures.Future()
    future.set_result(result)
    return future

def main(args):
    logging.info("Initial Database...")
    init_db()
    logging.info("Install ChromeDriverManager...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(10)
    logging.info("Open URL:[{}]".format(args.url))
    driver.get(args.url)
    try:
        search = driver.find_element(By.XPATH, INPUTKEY)
        goals = args.value.split(" ")
        logging.info("Search:[{}]".format(args.value))
        search.send_keys(args.value)
        search.send_keys(Keys.ENTER)
        blocks = driver.find_elements(By.XPATH, BLOCKCLASS)
        data = []
        for block in blocks:
            item = block.find_element(By.CLASS_NAME, TEXTCLASS)
            price = block.find_element(By.CLASS_NAME, PRICECLASS)
            addr = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            check_list = [ txt in item.text for txt in goals]
            if all(check_list):
                item_name = "-".join(item.text.split(" "))
                logging.info(f'{item_name} - {addr} - {price.text}')
                data.append({"item":str(item_name), "price":int(price.text)})
        check = thread_pool(batch_insert, data)
        if check:
            logging.info("Output CSV:[{}]".format(CSV_PATH))
            db_to_csv(CSV_PATH, "gpu")

    except Exception as e:
        logging.error(e)

    driver.quit()
    
if __name__ == '__main__':
    # Create log
    logger('./main.log', 'w', "info")
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)