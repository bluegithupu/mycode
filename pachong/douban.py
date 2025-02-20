import csv
from time import sleep
from playwright.sync_api import sync_playwright

def scrape_douban_top250():
    with sync_playwright() as p:
        # 启动浏览器（建议使用 Chromium）
        browser = p.chromium.launch(headless=True)  # headless=False 可以看到浏览器操作
        page = browser.new_page()
        
        # 设置用户代理和语言
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        })

        # 创建CSV文件，用于存储抓取的数据
        with open('douban_top250.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 写入CSV文件的表头
            writer.writerow(['排名', '标题', '评分', '评分人数', '短评', '详情链接'])

            # 处理分页（共10页）
            for page_num in range(10):
                # 构建每一页的URL
                url = f'https://movie.douban.com/top250?start={page_num * 25}'
                page.goto(url)  # 访问指定的URL
                page.wait_for_selector('.item')  # 等待内容加载

                # 提取数据
                items = page.query_selector_all('.item')  # 获取所有电影条目
                for index, item in enumerate(items):
                    rank = page_num * 25 + index + 1  # 计算实际排名
                    
                    # 标题（处理可能存在的多个标题）
                    title_element = item.query_selector('.title')
                    title = title_element.inner_text().strip() if title_element else ''  # 获取标题文本并去除多余空格

                    # 评分
                    rating = item.query_selector('.rating_num').inner_text().strip()  # 获取评分并去除多余空格
                    
                    # 评分人数
                    votes = item.query_selector('.star span').inner_text().replace('人评价', '')  # 获取评分人数并去掉单位
                    
                    # 短评（可能不存在）
                    quote_element = item.query_selector('.inq')
                    quote = quote_element.inner_text().strip() if quote_element else ''  # 获取短评文本并去除多余空格
                    
                    # 详情链接
                    link = item.query_selector('a').get_attribute('href')  # 获取详情链接

                    # 将抓取的数据写入CSV文件
                    writer.writerow([rank, title, rating, votes, quote, link])
                    print(f'已抓取：{rank} | {title}')  # 输出抓取信息

                # 添加随机延迟（2-5秒）避免被封
                sleep(3)
                print(f'已完成第 {page_num + 1}/10 页')  # 输出当前页数

        browser.close()  # 关闭浏览器
        print('全部数据已保存到 douban_top250.csv')  # 输出完成信息

if __name__ == '__main__':
    scrape_douban_top250()  # 调用主函数开始抓取