chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "GET_PAGE_CONTEXT") {
      sendResponse({
        title: document.title,
        url: window.location.href
      });
    }
  });