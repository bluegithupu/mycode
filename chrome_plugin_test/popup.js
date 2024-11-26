document.getElementById('extractText').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('edge://')) {
    alert('无法在浏览器内部页面上执行此操作');
    return;
  }
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: () => {
      const text = document.body.innerText;
      alert('提取的文本:\n' + text.substring(0, 500) + '...');
    }
  });
});

document.getElementById('changeBackground').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('edge://')) {
    alert('无法在浏览器内部页面上执行此操作');
    return;
  }
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: () => {
      document.body.style.backgroundColor = 
        document.body.style.backgroundColor === 'yellow' ? '' : 'yellow';
    }
  });
});