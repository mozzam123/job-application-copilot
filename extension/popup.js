const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");

const questionInput = document.getElementById("question");

const status = document.getElementById("status");
const answer = document.getElementById("answer");
const answerContainer = document.getElementById("answerContainer");


generateBtn.addEventListener("click", async () => {

  const question = questionInput.value.trim();

  if (!question) {
    status.textContent = "Please enter an application question.";
    return;
  }


  generateBtn.disabled = true;

  status.textContent = "Generating answer...";

  answer.textContent = "";
  answerContainer.style.display = "none";
  copyBtn.style.display = "none";


  try {

    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true
    });


    const extractionResponse = await chrome.tabs.sendMessage(
      tab.id,
      {
        type: "GET_JOB_CONTEXT"
      }
    );


    if (!extractionResponse.success) {
      throw new Error(
        extractionResponse.error || "Could not read this job."
      );
    }


    const response = await fetch(
      "http://127.0.0.1:8000/generate",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          question: question,
          job: extractionResponse.data
        })
      }
    );


    if (!response.ok) {

      const errorData = await response.json();

      throw new Error(
        errorData.detail || "Could not generate answer."
      );
    }


    const data = await response.json();


    answer.textContent = data.answer;

    answerContainer.style.display = "block";
    copyBtn.style.display = "block";

    status.textContent = "";


  } catch (error) {

    console.error(error);

    status.textContent = `Error: ${error.message}`;

  } finally {

    generateBtn.disabled = false;
  }
});


copyBtn.addEventListener("click", async () => {

  const text = answer.textContent.trim();

  if (!text) {
    return;
  }


  try {

    await navigator.clipboard.writeText(text);

    copyBtn.textContent = "Copied!";


    setTimeout(() => {
      copyBtn.textContent = "Copy Answer";
    }, 1500);


  } catch (error) {

    console.error(error);

    status.textContent = "Could not copy the answer.";
  }
});