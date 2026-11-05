import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WhatsAppBannHammer:
    def __init__(self, target_number):
        self.target = target_number
        # إعداد المتصفح ليظهر كأنه جهاز عادي
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=Automation")
        # نستخدم ChromeDriver الافتراضي الذي سيتم تثبيته لاحقًا
        self.driver = webdriver.Chrome(options=self.options)

    def start_scan(self):
        print("[+] Starting WhatsApp Ban Hammer...")
        print("[+] Please scan QR Code in the browser window...")
        
        # فتح واتساب ويب مع رقم المستهدف مباشرة
        self.driver.get("https://web.whatsapp.com/send?phone=" + str(self.target))
        
        # انتظار المسح
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_3Fmc-"))
            )
            print("[+] Scan Successful! Waiting for chat to load...")
            time.sleep(5) 
        except TimeoutException:
            print("[-] QR Code not scanned or timed out.")
            return

        self.ban_process()

    def ban_process(self):
        print("[+] Entering Report/Ban phase...")
        attempts = 0
        max_attempts = 20 # عدد مرات الضغط على زر الإبلاغ
        
        while attempts < max_attempts:
            try:
                # محاولة العثور على زر القائمة (النقاط الثلاث)
                menu_button = self.driver.find_element(By.XPATH, "//span[@data-icon='more']")
                menu_button.click()
                time.sleep(1)

                # محاولة العثور على خيار الإبلاغ (Report)
                report_option = self.driver.find_element(By.XPATH, "//span[text()='Report contact']")
                report_option.click()
                time.sleep(1)

                # تأكيد الإجراء (Confirm)
                confirm_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Report Contact']")
                confirm_btn.click()
                
                attempts += 1
                print(f"[+] Ban attempt {attempts}/{max_attempts} sent successfully!")
                
                # تأخير عشوائي بين كل محاولة
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"[-] Error during attempt {attempts}: {e}")
                break
        
        print("[+] Process finished. Check your WhatsApp account. The target number should be banned soon.")
        input("Press Enter to close browser...")
        self.driver.quit()

if __name__ == "__main__":
    target_num = input("Enter target number with country code (e.g., 9665xxxxxxxx): ")
    bot = WhatsAppBannHammer(target_num)
    bot.start_scan()
