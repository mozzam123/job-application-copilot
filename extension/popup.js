const extractBtn = document.getElementById("extractBtn");
const result = document.getElementById("result");

extractBtn.addEventListener("click", async () => {

  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  try {

    const response = await chrome.tabs.sendMessage(tab.id, {
      type: "GET_JOB_CONTEXT"
    });

    if (!response.success) {
      throw new Error(response.error);
    }

    const job = response.data;

    result.textContent = `
Company:
${job.company_name || "Not found"}

Job Title:
${job.job_title || "Not found"}

Company Description:
${job.company_description || "Not found"}

Job Description:
${job.job_description || "Not found"}

Requirements:
${job.requirements || "Not found"}
    `.trim();

  } catch (error) {

    console.error(error);

    result.textContent =
      "Could not extract job information from this page.";
  }
});