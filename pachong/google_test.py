from playwright.sync_api import sync_playwright
import time
import random

try:
    with sync_playwright() as p:
        # 启动浏览器，添加更多参数模拟真实用户
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--start-maximized',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            geolocation={'latitude': 39.9042, 'longitude': 116.4074},  # 北京坐标
            permissions=['geolocation']
        )
        
        page = context.new_page()

        # 注入一些随机的鼠标移动
        page.evaluate('''() => {
            const randomMove = () => {
                const event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': Math.random() * window.innerWidth,
                    'clientY': Math.random() * window.innerHeight
                });
                document.dispatchEvent(event);
            };
            setInterval(randomMove, 2000);
        }''')

        print("正在访问 Google...")
        url = "https://www.google.com"
        page.goto(url, wait_until='networkidle')
        time.sleep(random.uniform(2, 4))

        # 随机鼠标移动
        page.mouse.move(random.randint(100, 700), random.randint(100, 500))
        time.sleep(random.uniform(1, 2))
        
        print("等待搜索框加载...")
        search_box = page.wait_for_selector('textarea[name="q"]', timeout=30000)
        
        # 模拟真实点击
        box = search_box.bounding_box()
        page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        time.sleep(random.uniform(0.5, 1))
        page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        time.sleep(random.uniform(0.5, 1))

        print("输入搜索关键词...")
        search_text = '北京今天的天气'
        for char in search_text:
            search_box.type(char)
            time.sleep(random.uniform(0.1, 0.4))  # 随机输入延迟

        time.sleep(random.uniform(1, 2))
        
        # 模拟人工输入
        search_text = '北京今天的天气'
        for char in search_text:
            search_box.type(char)
            time.sleep(0.3)  # 每个字符之间添加随机延迟
        # search_box.fill('北京今天的天气')
        time.sleep(1)  # 添加短暂延迟
        
        print("点击搜索按钮...")
        page.keyboard.press('Enter')
        
        # 等待搜索结果加载
        print("等待搜索结果加载...")
        page.wait_for_load_state('networkidle')
        time.sleep(2)  # 添加额外等待时间
        
        # 保存搜索结果页面截图
        # page.screenshot(path="search_results.png")
        
        # 尝试多个可能的选择器
        selectors = ['div.g', 'div[class*="g"]', 'div[data-hveid]']
        first_result = None
        
        for selector in selectors:
            print(f"尝试使用选择器: {selector}")
            first_result = page.query_selector(selector)
            if first_result:
                result_text = first_result.inner_text()
                print("第一条搜索结果:", result_text)
                break
        
        if not first_result:
            print("未能找到搜索结果，请检查选择器")
        
        # 关闭浏览器
        browser.close()

except Exception as e:
    print(f"发生错误: {str(e)}")
