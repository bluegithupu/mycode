import pyautogui
import time

def auto_like():
    while True:
        # 查找当前屏幕可见的点赞按钮
        buttons = list(pyautogui.locateAllOnScreen('agree1.png', confidence=0.8))
        
        if buttons:
            for btn in buttons:
                x, y = pyautogui.center(btn)
                pyautogui.click(x, y)
                time.sleep(0.5)  # 防止操作过快被限制
            print(f'已点赞 {len(buttons)} 篇文章')
        else:
            # 无按钮时滚动加载新内容
            pyautogui.scroll(-800)
            time.sleep(2)  # 等待新内容加载

# 启动前提示
pyautogui.alert('即将开始自动化操作，请确保：\n1.浏览器窗口置顶\n2.页面已打开到文章列表', '准备就绪')

try:
    auto_like()
except KeyboardInterrupt:
    pyautogui.alert('程序已终止', '提示')