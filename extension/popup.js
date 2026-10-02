const extractBtn = document.getElementById("extractBtn");
const result = document.getElementById("result");

extractBtn.addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  try {
    const response = await chrome.tabs.sendMessage(tab.id, {
      type: "GET_PAGE_CONTEXT"
    });

    result.textContent =
      `Title: ${response.title}\n\n` +
      `URL: ${response.url}`;

  } catch (error) {
    result.textContent =
      "Could not read this page. Make sure you are on Wellfound.";
  }
});