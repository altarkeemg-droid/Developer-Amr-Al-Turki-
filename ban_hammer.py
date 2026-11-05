import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WhatsAppAccountCloser:
    def __init__(self, target_number):
        self.target = target_number
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=Automation")
        self.driver = webdriver.Chrome(options=self.options)

    def start_close(self):
        print("[+] Starting WhatsApp Account Closer...")
        print("[+] Please scan QR Code in the browser window...")
        
        # فتح واتساب ويب مع رقم المستهدف
        self.driver.get("https://web.whatsapp.com/send?phone=" + str(self.target))
        
        try:
            # انتظار تحميل الشات
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_3Fmc-"))
            )
            print("[+] Chat Loaded! Starting Ban Process...")
            time.sleep(5) 
        except TimeoutException:
            print("[-] QR Code not scanned or timed out.")
            return

        self.close_account()

    def close_account(self):
        attempts = 0
        max_attempts = 30  # زيادة عدد البلاغات لزيادة فرص الإغلاق
        
        while attempts < max_attempts:
            try:
                # فتح القائمة
                menu_button = self.driver.find_element(By.XPATH, "//span[@data-icon='more']")
                menu_button.click()
                time.sleep(1)

                # الضغط على Report
                report_option = self.driver.find_element(By.XPATH, "//span[text()='Report contact']")
                report_option.click()
                time.sleep(1)

                # تأكيد الإبلاغ
                confirm_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Report Contact']")
                confirm_btn.click()
                
                attempts += 1
                print(f"[+] Attempt {attempts}/{max_attempts} sent. Closing account...")
                
                # تأخير عشوائي لمحاكاة سلوك بشري
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"[-] Error at attempt {attempts}: {e}")
                break
        
        print("[+] Process finished. The account should be closed/banned shortly.")
        input("Press Enter to close browser...")
        self.driver.quit()

if __name__ == "__main__":
    target_num = input("Enter target number with country code (e.g., 9665xxxxxxxx): ")
    bot = WhatsAppAccountCloser(target_num)
    bot.start_close()
