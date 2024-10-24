# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import privacy

import time

# iPhone 16pro max デザートチタニウム 512Gb
url = "https://www.apple.com/jp/shop/buy-iphone/iphone-16-pro/6.9%E3%82%A4%E3%83%B3%E3%83%81%E3%83%87%E3%82%A3%E3%82%B9%E3%83%97%E3%83%AC%E3%82%A4-512gb-%E3%83%87%E3%82%B6%E3%83%BC%E3%83%88%E3%83%81%E3%82%BF%E3%83%8B%E3%82%A6%E3%83%A0-sim%E3%83%95%E3%83%AA%E3%83%BC"

appleid_username = privacy.appleid_username
appleid_password = privacy.appleid_password
phone_nnumber = privacy.phone_nnumber
cvv_credit = privacy.cvv_credit

# options = webdriver.ChromeOptions()
# ブラウザ·オブジェクトの作成
# driver = webdriver.Chrome(options=options)

# Setup Chrome options
options = Options()
options.add_argument('--remote-debugging-pipe') 
# 初期化設定の追加 (実行が完了してもブラウザは自動的に閉じないらしい)
options.add_experimental_option('detach', True)
# options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser navigating.

# Set path to chromedriver as a service
webdriver_service = Service(ChromeDriverManager().install())
# Set the driver
driver = webdriver.Chrome(service=webdriver_service, options=options)


def one():
    # 下取り選択
    while True:
        try:
            # 「下取りを利用しない」要素の選択？
            element_old = driver.find_element(By.ID, 'noTradeIn_label')
            break
        except NoSuchElementException:
            driver.refresh()

    driver.execute_script("arguments[0].click();", element_old)

    # Applecare選択
    element_care = driver.find_element(By.ID, 'applecareplus_59_noapplecare')
    driver.execute_script("arguments[0].click();", element_care)

    # バッグへの追加
    time.sleep(1)
    element_car = driver.find_element(By.XPATH,
                                       '//*[@id="root"]/div[2]/div[3]/div[8]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/span/form/div/span/button')
    # if element_car is not True:
    #     element_car = driver.find_element(By.XPATH,
    #                                       '//*[@id="root"]/div[2]/div[3]/div[4]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/span/form/div/span/button')
    driver.execute_script("arguments[0].click();", element_car)


# iPhone選択画面への遷移
driver.get(url)
driver.implicitly_wait(20)

one()
if driver.current_url == url:
    one()

# iPhone追加後のショッピングバッグへの遷移
driver.implicitly_wait(10)
element_check = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/form/button')
driver.execute_script("arguments[0].click();", element_check)

# 注文手続きへの遷移
driver.implicitly_wait(10)
element_check_out = driver.find_element(By.XPATH, '//*[@id="shoppingCart.actions.navCheckout"]')
driver.execute_script("arguments[0].click();", element_check_out)

# チェックアウトの待ち時間のために長めに準備(ここは非同期処理で最適化できそう)
driver.implicitly_wait(30)

# iframe変換
iframe = driver.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
driver.switch_to.frame(iframe)
# apple IDの入力
driver.implicitly_wait(10)
element_username = driver.find_element(By.XPATH,'//*[@id="account_name_text_field"]')
element_username.send_keys(appleid_username)
## apple IDのクリック
time.sleep(3)
user_name_enter = driver.find_element(By.XPATH, '//*[@id="sign-in"]')
driver.execute_script("arguments[0].click();", user_name_enter)


# パスワード入力
element_password = driver.find_element(By.XPATH,'//*[@id="password_text_field"]')
element_password.send_keys(appleid_password)
## ユーザーネームクリック
password_enter = driver.find_element(By.XPATH, '//*[@id="sign-in"]')
driver.execute_script("arguments[0].click();", password_enter)

# end of iframe
driver.switch_to.default_content()
# 配送選択※ピックアップなら自身で受け取るで対応
choice_delivery = driver.find_element(By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')
driver.execute_script("arguments[0].click();", choice_delivery)

# 電話番号入力
element_phone_number = driver.find_element(By.XPATH,'//*[@id="checkout.shipping.addressContactPhone.address.mobilePhone"]')
element_phone_number.send_keys(phone_nnumber)
# 支払い画面への遷移
payment_transition = driver.find_element(By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')
driver.execute_script("arguments[0].click();", payment_transition)

# 決済情報入力
driver.implicitly_wait(10)
chocie_credit_card = driver.find_element(By.XPATH, '//*[@id="checkout.billing.billingoptions.saved_card"]')
driver.execute_script("arguments[0].click();", chocie_credit_card)
# クレジットカードのCVV入力
element_cvv = driver.find_element(By.XPATH,'//*[@id="checkout.billing.billingOptions.selectedBillingOptions.savedCard.cardInputs.cardInput-0.securityCode"]')
element_cvv.send_keys(cvv_credit)

# 注文確認画面への遷移
check_order_transition = driver.find_element(By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')
driver.execute_script("arguments[0].click();", check_order_transition)

# debug
# monitor scroll
for i in range(10):
    driver.execute_script('window.scrollBy(0, 100);')
    print('下へ移動しました')
    time.sleep(1)


# 注文確認画面への遷移
check_order = driver.find_element(By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')
driver.execute_script("arguments[0].click();", check_order)

# Take a screenshot
driver.save_screenshot("screenshot.png")

# Quit the driver
driver.implicitly_wait(20)
driver.quit()
