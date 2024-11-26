chrome.runtime.onInstalled.addListener(() => {
  console.log('插件已安装');
});

// 监听来自popup或content script的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'getPageInfo') {
    sendResponse({ success: true });
  }
}); 