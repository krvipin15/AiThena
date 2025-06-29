const API_BASE = "http://localhost:8000";
let sessionData = {
  pdfSummaries: [],
  youtubeContent: {},
  customText: "",
  customSummary: "",
  generatedFlashcards: [],
  quizData: null,
  quizResults: null,
};

// Check authentication
document.addEventListener("DOMContentLoaded", function () {
  const userEmail = localStorage.getItem("userEmail");
  const userPassword = localStorage.getItem("userPassword");

  if (!userEmail || !userPassword) {
    window.location.href = "login.html";
    return;
  }

  document.getElementById("userEmail").textContent = userEmail;
  setupEventListeners();
  setupTabs();
});

function setupEventListeners() {
  // Logout
  document.getElementById("logoutBtn").addEventListener("click", logout);

  // PDF upload - FIXED
  document.getElementById("uploadPdfBtn").addEventListener("click", () => {
    document.getElementById("pdfFileInput").click();
  });
  document
    .getElementById("pdfFileInput")
    .addEventListener("change", handlePdfUpload);

  // YouTube processing
  document
    .getElementById("processYoutubeBtn")
    .addEventListener("click", handleYoutubeProcess);

  // Text summarization
  document
    .getElementById("summarizeBtn")
    .addEventListener("click", handleTextSummarization);

  // Flashcards generation
  document
    .getElementById("generateFlashcardsBtn")
    .addEventListener("click", handleFlashcardsGeneration);

  // Quiz generation
  document
    .getElementById("generateQuizBtn")
    .addEventListener("click", handleQuizGeneration);

  // Source selection handlers
  document
    .getElementById("flashcardSource")
    .addEventListener("change", updateFlashcardSource);
  document
    .getElementById("quizSource")
    .addEventListener("change", updateQuizSource);
}

function setupTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const tabName = btn.getAttribute("data-tab");

      // Update tab styling
      tabBtns.forEach((tab) => {
        tab.classList.remove("active");
      });
      btn.classList.add("active");

      // Show content
      tabContents.forEach((content) => content.classList.remove("active"));
      document.getElementById(tabName + "Content").classList.add("active");
    });
  });
}

function logout() {
  localStorage.removeItem("userEmail");
  localStorage.removeItem("userPassword");
  window.location.href = "index.html";
}

// FIXED: PDF Upload Function
async function handlePdfUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const resultsDiv = document.getElementById("pdfResults");
  showLoading(resultsDiv, "Processing PDF... This may take a few minutes.");

  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("email", localStorage.getItem("userEmail"));
    formData.append("password", localStorage.getItem("userPassword"));

    const response = await fetch(`${API_BASE}/upload_pdf`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();

      if (result && result.summaries) {
        sessionData.pdfSummaries = result.summaries;
        displayPdfResults(result.summaries);
      } else {
        showError(resultsDiv, "No summaries generated from PDF");
      }
    } else {
      const errorText = await response.text();
      console.error("PDF upload error:", errorText);
      showError(
        resultsDiv,
        `Error uploading PDF: ${response.status} ${response.statusText}`
      );
    }
  } catch (error) {
    console.error("PDF upload error:", error);
    showError(resultsDiv, "Error uploading PDF: " + error.message);
  }
}

async function handleYoutubeProcess() {
  const url = document.getElementById("youtubeUrl").value.trim();
  if (!url) {
    alert("Please enter a YouTube URL");
    return;
  }

  const resultsDiv = document.getElementById("youtubeResults");
  showLoading(resultsDiv, "Processing YouTube video...");

  try {
    const formData = new FormData();
    formData.append("youtube_url", url);
    formData.append("email", localStorage.getItem("userEmail"));
    formData.append("password", localStorage.getItem("userPassword"));

    const response = await fetch(`${API_BASE}/process_youtube`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();

      if (result && result.summary) {
        sessionData.youtubeContent = {
          transcript: result.transcript || "",
          summary: result.summary,
        };
        displayYoutubeResults(result);
      } else {
        showError(resultsDiv, "Error processing YouTube video");
      }
    } else {
      showError(resultsDiv, `Error: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    showError(resultsDiv, "Error processing YouTube video: " + error.message);
  }
}

async function handleTextSummarization() {
  const text = document.getElementById("textToSummarize").value.trim();
  if (!text) {
    alert("Please enter text to summarize");
    return;
  }

  const resultsDiv = document.getElementById("textResults");
  showLoading(resultsDiv, "Generating summary...");

  try {
    const formData = new FormData();
    formData.append("text", text);
    formData.append("email", localStorage.getItem("userEmail"));
    formData.append("password", localStorage.getItem("userPassword"));

    const response = await fetch(`${API_BASE}/summarize`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();

      if (result && result.summary) {
        sessionData.customText = text;
        sessionData.customSummary = result.summary;
        displayTextResults(result);
      } else {
        showError(resultsDiv, "Error generating summary");
      }
    } else {
      showError(resultsDiv, `Error: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    showError(resultsDiv, "Error generating summary: " + error.message);
  }
}

async function handleFlashcardsGeneration() {
  const source = document.getElementById("flashcardSource").value;
  let text = "";

  if (source === "custom") {
    text = document.getElementById("flashcardText").value.trim();
  } else if (source === "pdf") {
    text = sessionData.pdfSummaries.map((s) => s.summary).join("\n");
  } else if (source === "youtube") {
    text = sessionData.youtubeContent.summary || "";
  }

  if (!text) {
    alert("Please enter text or select a content source");
    return;
  }

  const resultsDiv = document.getElementById("flashcardsResults");
  showLoading(resultsDiv, "Creating flashcards...");

  try {
    const formData = new FormData();
    formData.append("text", text);
    formData.append("email", localStorage.getItem("userEmail"));
    formData.append("password", localStorage.getItem("userPassword"));

    const response = await fetch(`${API_BASE}/generate_flashcards`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();

      if (result && result.flashcards) {
        sessionData.generatedFlashcards = result.flashcards;
        displayFlashcards(result.flashcards);
      } else {
        showError(resultsDiv, "Error generating flashcards");
      }
    } else {
      showError(resultsDiv, `Error: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    showError(resultsDiv, "Error generating flashcards: " + error.message);
  }
}

async function handleQuizGeneration() {
  const source = document.getElementById("quizSource").value;
  let text = "";

  if (source === "custom") {
    text = document.getElementById("quizText").value.trim();
  } else if (source === "pdf") {
    text = sessionData.pdfSummaries.map((s) => s.summary).join("\n");
  } else if (source === "youtube") {
    text = sessionData.youtubeContent.summary || "";
  }

  if (!text) {
    alert("Please enter text or select a content source");
    return;
  }

  const resultsDiv = document.getElementById("quizResults");
  showLoading(resultsDiv, "Creating quiz...");

  try {
    const formData = new FormData();
    formData.append("text", text);
    formData.append("email", localStorage.getItem("userEmail"));
    formData.append("password", localStorage.getItem("userPassword"));

    const response = await fetch(`${API_BASE}/generate_mcq`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();

      if (result && result.mcqs) {
        sessionData.quizData = result.mcqs;
        displayQuiz(result.mcqs);
      } else {
        showError(resultsDiv, "Error generating quiz");
      }
    } else {
      showError(resultsDiv, `Error: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    showError(resultsDiv, "Error generating quiz: " + error.message);
  }
}

function updateFlashcardSource() {
  const source = document.getElementById("flashcardSource").value;
  const textArea = document.getElementById("flashcardText");

  if (source === "pdf" && sessionData.pdfSummaries.length > 0) {
    textArea.value = sessionData.pdfSummaries.map((s) => s.summary).join("\n");
    textArea.disabled = true;

    // Show info
    const container = textArea.parentNode;
    let infoDiv = container.querySelector(".content-source-info");
    if (!infoDiv) {
      infoDiv = document.createElement("div");
      infoDiv.className = "content-source-info";
      container.insertBefore(infoDiv, textArea);
    }
    infoDiv.innerHTML = `📚 Using ${sessionData.pdfSummaries.length} PDF chapter summaries`;
  } else if (source === "youtube" && sessionData.youtubeContent.summary) {
    textArea.value = sessionData.youtubeContent.summary;
    textArea.disabled = true;

    // Show info
    const container = textArea.parentNode;
    let infoDiv = container.querySelector(".content-source-info");
    if (!infoDiv) {
      infoDiv = document.createElement("div");
      infoDiv.className = "content-source-info";
      container.insertBefore(infoDiv, textArea);
    }
    infoDiv.innerHTML = "🎥 Using YouTube video summary";
  } else {
    textArea.value = "";
    textArea.disabled = false;

    // Remove info
    const container = textArea.parentNode;
    const infoDiv = container.querySelector(".content-source-info");
    if (infoDiv) {
      infoDiv.remove();
    }
  }
}

function updateQuizSource() {
  const source = document.getElementById("quizSource").value;
  const textArea = document.getElementById("quizText");

  if (source === "pdf" && sessionData.pdfSummaries.length > 0) {
    textArea.value = sessionData.pdfSummaries.map((s) => s.summary).join("\n");
    textArea.disabled = true;

    // Show info
    const container = textArea.parentNode;
    let infoDiv = container.querySelector(".content-source-info");
    if (!infoDiv) {
      infoDiv = document.createElement("div");
      infoDiv.className = "content-source-info";
      container.insertBefore(infoDiv, textArea);
    }
    infoDiv.innerHTML = `📚 Using ${sessionData.pdfSummaries.length} PDF chapter summaries`;
  } else if (source === "youtube" && sessionData.youtubeContent.summary) {
    textArea.value = sessionData.youtubeContent.summary;
    textArea.disabled = true;

    // Show info
    const container = textArea.parentNode;
    let infoDiv = container.querySelector(".content-source-info");
    if (!infoDiv) {
      infoDiv = document.createElement("div");
      infoDiv.className = "content-source-info";
      container.insertBefore(infoDiv, textArea);
    }
    infoDiv.innerHTML = "🎥 Using YouTube video summary";
  } else {
    textArea.value = "";
    textArea.disabled = false;

    // Remove info
    const container = textArea.parentNode;
    const infoDiv = container.querySelector(".content-source-info");
    if (infoDiv) {
      infoDiv.remove();
    }
  }
}

function displayPdfResults(summaries) {
  const resultsDiv = document.getElementById("pdfResults");
  let html = '<div style="margin-top: 1rem;">';

  html += `<div class="result-container">
        <h4>✅ PDF processed successfully! Generated ${summaries.length} summaries.</h4>
    </div>`;

  html +=
    '<h4 style="color: #0d121c; font-weight: 700; margin: 1.5rem 0 1rem 0;">📝 Chapter Summaries</h4>';

  summaries.forEach((summary, index) => {
    html += `
            <div class="result-container">
                <h4>📖 Chapter ${index + 1}: ${summary.title || "Untitled"}</h4>
                <p style="line-height: 1.6;">${
                  summary.summary || "No summary available"
                }</p>
            </div>
        `;
  });

  // Combined summary
  html +=
    '<h4 style="color: #0d121c; font-weight: 700; margin: 1.5rem 0 1rem 0;">🔗 Combined Summary</h4>';
  let combinedText = "";
  summaries.forEach((summary) => {
    combinedText += `**${summary.title || "Untitled"}:**\n${
      summary.summary || ""
    }\n\n`;
  });

  html += `
        <div class="result-container">
            <textarea readonly style="width: 100%; height: 300px; padding: 1rem; border: 1px solid #e7eaed; border-radius: 0.5rem; font-size: 0.9rem; line-height: 1.5;">${combinedText}</textarea>
        </div>
    `;

  html += "</div>";
  resultsDiv.innerHTML = html;
  resultsDiv.style.display = "block";
}

function displayYoutubeResults(result) {
  const resultsDiv = document.getElementById("youtubeResults");
  resultsDiv.innerHTML = `
        <div style="margin-top: 1rem;">
            <div class="result-container">
                <h4>✅ Video processed successfully!</h4>
            </div>
            
            <details style="margin: 1rem 0;">
                <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: #f8f9fb; border-radius: 0.5rem;">📝 View Full Transcript</summary>
                <div class="result-container" style="margin-top: 0.5rem;">
                    <textarea readonly style="width: 100%; height: 200px; padding: 1rem; border: 1px solid #e7eaed; border-radius: 0.5rem; font-size: 0.9rem;">${
                      result.transcript || "Transcript not available"
                    }</textarea>
                </div>
            </details>
            
            <h4 style="color: #0d121c; font-weight: 700; margin: 1rem 0;">✨ AI-Generated Summary</h4>
            <div class="result-container">
                <p style="line-height: 1.6;">${result.summary}</p>
            </div>
        </div>
    `;
  resultsDiv.style.display = "block";
}

function displayTextResults(result) {
  const resultsDiv = document.getElementById("textResults");
  resultsDiv.innerHTML = `
        <div style="margin-top: 1rem;">
            <div class="result-container">
                <h4>✅ Summary generated!</h4>
            </div>
            
            <h4 style="color: #0d121c; font-weight: 700; margin: 1rem 0;">📝 AI Summary</h4>
            <div class="result-container">
                <p style="line-height: 1.6;">${result.summary}</p>
            </div>
        </div>
    `;
  resultsDiv.style.display = "block";
}

function displayFlashcards(flashcards) {
  const resultsDiv = document.getElementById("flashcardsResults");
  let html = `
        <div style="margin-top: 1rem;">
            <div class="result-container">
                <h4>✅ Generated ${flashcards.length} flashcards!</h4>
            </div>
            
            <h4 style="color: #0d121c; font-weight: 700; margin: 1rem 0;">🎯 Your Flashcards</h4>
    `;

  flashcards.forEach((card, index) => {
    html += `
            <div class="flashcard">
                <div class="flashcard-question">❓ Q${index + 1}: ${
      card.question
    }</div>
                <div class="flashcard-answer">💡 ${card.answer}</div>
            </div>
        `;
  });

  html += "</div>";
  resultsDiv.innerHTML = html;
  resultsDiv.style.display = "block";
}

function displayQuiz(mcqs) {
  const resultsDiv = document.getElementById("quizResults");
  let html = `
        <div style="margin-top: 1rem;">
            <div class="result-container">
                <h4>✅ Quiz generated! Answer the questions below.</h4>
            </div>
            
            <div class="quiz-progress">
                📊 Progress: 0/${mcqs.length} questions answered
            </div>
            
            <form id="quizForm">
    `;

  mcqs.forEach((mcq, index) => {
    html += `
            <div class="quiz-question">
                <h4>Question ${index + 1}: ${mcq.question}</h4>
                <div class="radio-group">
        `;

    mcq.choices.forEach((choice, choiceIndex) => {
      const letter = String.fromCharCode(65 + choiceIndex);
      html += `
                <label class="radio-option">
                    <input type="radio" name="q${index}" value="${choice}" onchange="updateQuizProgress()">
                    <span>${letter}) ${choice}</span>
                </label>
            `;
    });

    html += `
                </div>
            </div>
        `;
  });

  html += `
            <button type="button" onclick="submitQuiz()" class="btn-primary" style="width: 100%; margin-top: 1rem;">
                🎯 Submit Quiz
            </button>
        </form>
    </div>`;

  resultsDiv.innerHTML = html;
  resultsDiv.style.display = "block";
}

function updateQuizProgress() {
  const form = document.getElementById("quizForm");
  if (!form) return;

  const totalQuestions = sessionData.quizData.length;
  const answeredQuestions = form.querySelectorAll(
    'input[type="radio"]:checked'
  ).length;

  const progressDiv = document.querySelector(".quiz-progress");
  if (progressDiv) {
    progressDiv.innerHTML = `📊 Progress: ${answeredQuestions}/${totalQuestions} questions answered`;
  }
}

function submitQuiz() {
  const form = document.getElementById("quizForm");
  if (!form) return;

  const totalQuestions = sessionData.quizData.length;
  const answeredQuestions = form.querySelectorAll(
    'input[type="radio"]:checked'
  );

  if (answeredQuestions.length !== totalQuestions) {
    alert(
      `Please answer all questions. (${answeredQuestions.length}/${totalQuestions} completed)`
    );
    return;
  }

  let correct = 0;
  let results = {};

  answeredQuestions.forEach((input, index) => {
    const questionIndex = parseInt(input.name.replace("q", ""));
    const userAnswer = input.value;
    const correctAnswer = sessionData.quizData[questionIndex].answer;

    const isCorrect = userAnswer.startsWith(correctAnswer);
    if (isCorrect) correct++;

    results[questionIndex] = {
      question: sessionData.quizData[questionIndex].question,
      userAnswer: userAnswer,
      correctAnswer: correctAnswer,
      isCorrect: isCorrect,
    };
  });

  const score = (correct / totalQuestions) * 100;
  sessionData.quizResults = { score, correct, totalQuestions, results };

  displayQuizResults(score, correct, totalQuestions);
  updateFeedbackTab();
}

function displayQuizResults(score, correct, total) {
  const resultsDiv = document.getElementById("quizResults");
  const scoreClass =
    score < 60 ? "low-score" : score < 80 ? "medium-score" : "";

  resultsDiv.innerHTML += `
        <div class="quiz-results ${scoreClass}" style="margin-top: 1rem;">
            <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">🎯 Quiz Results</h3>
            <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">Score: ${correct}/${total} (${score.toFixed(
    1
  )}%)</h2>
            <p style="margin: 0.5rem 0;">${
              score >= 80
                ? "🎉 Excellent!"
                : score >= 60
                ? "📚 Good effort!"
                : "💪 Keep studying!"
            }</p>
            <button onclick="generateFeedback()" class="btn-primary" style="margin-top: 1rem;">
                💡 Get AI Feedback
            </button>
        </div>
    `;
}

function updateFeedbackTab() {
  if (sessionData.quizResults) {
    const feedbackDiv = document.getElementById("feedbackResults");
    const { score, correct, totalQuestions } = sessionData.quizResults;
    const scoreClass =
      score < 60 ? "low-score" : score < 80 ? "medium-score" : "";

    feedbackDiv.innerHTML = `
            <div class="quiz-results ${scoreClass}">
                <h4 style="font-size: 1.125rem; font-weight: 700;">📈 Latest Performance</h4>
                <h3 style="font-size: 1.25rem; font-weight: 700;">Score: ${correct}/${totalQuestions} (${score.toFixed(
      1
    )}%)</h3>
                <button onclick="generateFeedback()" class="btn-primary" style="margin-top: 1rem;">
                    🤖 Get AI Feedback
                </button>
            </div>
        `;
  }
}

async function generateFeedback() {
  if (!sessionData.quizResults) return;

  const feedbackDiv = document.getElementById("feedbackResults");
  showLoading(feedbackDiv, "AI is analyzing your performance...");

  try {
    const { results, score, correct, totalQuestions } = sessionData.quizResults;
    let quizSummary = `Quiz Score: ${score.toFixed(
      1
    )}% (${correct}/${totalQuestions})\n\n`;

    Object.keys(results).forEach((i) => {
      const result = results[i];
      const correctSymbol = result.isCorrect ? "✓" : "✗";
      quizSummary += `Q${parseInt(i) + 1}: ${result.question}\n`;
      quizSummary += `Your Answer: ${result.userAnswer} ${correctSymbol}\n`;
      quizSummary += `Correct Answer: ${result.correctAnswer}\n\n`;
    });

    const formData = new FormData();
    formData.append("email", localStorage.getItem("userEmail"));
    formData.append("password", localStorage.getItem("userPassword"));
    formData.append("quiz_results", quizSummary);

    const response = await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();

      feedbackDiv.innerHTML = `
                <div class="result-container">
                    <h4 style="font-size: 1.125rem; font-weight: 700; margin-bottom: 1rem;">🎯 Your Personalized AI Feedback</h4>
                    <div style="white-space: pre-line; line-height: 1.6;">
                        ${result.feedback}
                    </div>
                </div>
            `;
    } else {
      showError(feedbackDiv, "Error generating feedback");
    }
  } catch (error) {
    showError(feedbackDiv, "Error generating feedback: " + error.message);
  }
}

function showLoading(element, message) {
  element.innerHTML = `
        <div class="result-container" style="text-align: center;">
            <div class="spinner"></div>
            <span>${message}</span>
        </div>
    `;
  element.style.display = "block";
}

function showError(element, message) {
  element.innerHTML = `
        <div class="result-container" style="background: #fee2e2; border-color: #fecaca; color: #dc2626;">
            <p>❌ ${message}</p>
        </div>
    `;
  element.style.display = "block";
}
