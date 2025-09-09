from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
 
 
# 定义用户名和密码
username = "学号"
password = "密码"
cid=['课程名称']
 
# 创建 Edge 浏览器的选项对象
options = Options()
# 让浏览器在脚本执行完后不自动关闭
options.add_experimental_option("detach", True)
# 启动 Edge 浏览器
driver = webdriver.Edge(options=options)
 
 
def login01():
    # 登录页面的 URL
    login_url = "https://byxt.buaa.edu.cn/"
    # 打开登录页面
    driver.get(login_url)
    # 最大化浏览器窗口
    driver.maximize_window()
    # 滚动到页面顶部
    driver.execute_script("window.scrollTo(0,0)")

    # 先切换到 iframe
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)
 
 
    # 等待并找到用户名输入框，输入用户名
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unPassword")))
    username_input.send_keys(username)
 
 
    # 等待并找到密码输入框，输入密码
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pwPassword")))
    password_input.send_keys(password)
 

    # 找到登录按钮，点击登录
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content-con"]/div[1]/div[7]/input')))
    login_button.click()
    # 等待3秒
    time.sleep(3)
 
 
def login02():
    # 第二阶段登录的 URL
    login_url02 = 'https://byxk.buaa.edu.cn/xsxk/profile/index.html'
    try:
        # 打开第二阶段登录页面
        driver.get(login_url02)
        
        define_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="xsxkapp"]/div[4]/div/div[3]/span/button[1]/span')))
        define_button.click()
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="stundentinfoDiv"]/button')))
        login_button.click()
    except:
        print('浏览器错误或其它错误')
        time.sleep(3)
 
 
def catch_coures(ans):
    try: 
        for attempt in range(5):  # 设定尝试抢课的次数，可以根据需要修改
            print(f"正在尝试第 {attempt + 1} 次抢课: {cid[0]}")       
            # 课程查询逻辑
            query_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="xsxkapp"]/div/div[3]/div[2]/div[6]/div/div[2]/div/input')))
            query_input.clear()
            query_input.send_keys(cid[0])  # 这里只抢一门课
            query_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="xsxkapp"]/div/div[3]/div[2]/button/span')))
            query_button.click()

            # 点击选课按钮
            catch_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div/div/div[18]/div/div/button[2]')))
            catch_button.click()

            xk_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[3]/button[2]/span')))
            xk_button.click()

            ans += f"第 {attempt + 1} 次尝试抢课: {cid[0]}\n"
            # 每次尝试后，等待一段时间再尝试
            time.sleep(1)  # 可以根据需要调整等待时间

        # 尝试多次后，刷新页面
        print(f"尝试 {cid[0]} 结束，正在刷新页面")
        driver.refresh()
        time.sleep(3)  # 刷新后等待3秒再继续尝试
    except Exception as e:
        print('选课过程中出现错误:', e)
    return ans

 
 
if __name__ == '__main__':
    # 存储已选课程的列表
    result_cid = []
    # 首次登录
    login01()
    while (1):
        # 尝试登录
        login02()
        ans = ''
        # 尝试选课
        bns = catch_coures(ans)
        print("所有课程情况：", bns)
        print('——————————————————————————————————————————')
        # 循环    
        time.sleep(3)
        continue