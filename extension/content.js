chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  if (request.type === "GET_JOB_CONTEXT") {

    try {
      const extractor = new WellfoundExtractor();

      const jobData = extractor.extract();

      sendResponse({
        success: true,
        data: jobData
      });

    } catch (error) {

      console.error("Extraction failed:", error);

      sendResponse({
        success: false,
        error: error.message
      });
    }
  }
});