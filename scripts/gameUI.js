// gameUI.js - UI updates and display logic

// DOM elements
let gameArea, verbGrid, answerInput, feedback, actionBtn;
let totalQuestionsEl, correctAnswersEl, percentageEl;

function initializeGameUI() {
  // Get DOM elements
  gameArea = document.getElementById("game-area");
  verbGrid = document.getElementById("verb-grid");
  answerInput = document.getElementById("answer-input");
  feedback = document.getElementById("feedback");
  actionBtn = document.getElementById("action-btn");
  totalQuestionsEl = document.getElementById("total-questions");
  correctAnswersEl = document.getElementById("correct-answers");
  percentageEl = document.getElementById("percentage");

  // Set up event listeners
  actionBtn.addEventListener("click", handleActionButton);

  // Set up back button event listener
  const backBtn = document.getElementById("back-btn");
  if (backBtn) {
    backBtn.addEventListener("click", goBackToIndex);
  }

  // Add document-level Enter key listener
  document.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault(); // Prevent default form submission behavior
      handleActionButton();
    }
  });
}

function displayVerb() {
  verbGrid.innerHTML = "";

  for (let i = 0; i < columnHeaders.length; i++) {
    // Create column container
    const column = document.createElement("div");
    column.className = "verb-column";

    // Create header
    const header = document.createElement("div");
    header.className = "verb-header";
    header.textContent = columnHeaders[i];

    // Create data cell
    const cell = document.createElement("div");
    cell.className = "verb-cell";

    if (i === hiddenColumn) {
      cell.className += " hidden-cell";
      cell.textContent = "???";
    } else {
      // Get the value for this column
      const value = currentVerb[columnHeaders[i]];
      cell.textContent = capitalizeFirstLetter(value);
    }

    // Add header and cell to column
    column.appendChild(header);
    column.appendChild(cell);

    // Add column to grid
    verbGrid.appendChild(column);
  }
}

function showFeedback(isCorrect, correctAnswer) {
  feedback.style.display = "block";

  if (isCorrect) {
    feedback.className = "feedback correct";
    feedback.textContent = "Correct! Well done!";
  } else {
    feedback.className = "feedback incorrect";
    const capitalizedAnswer = capitalizeFirstLetter(correctAnswer);
    feedback.textContent = `Incorrect. The correct answer is: "${capitalizedAnswer}"`;
  }

  // Show the complete verb by updating the existing grid
  revealAllVerbForms();
}

function revealAllVerbForms() {
  const existingColumns = verbGrid.querySelectorAll(".verb-column");

  for (let i = 0; i < columnHeaders.length; i++) {
    if (existingColumns[i]) {
      const cell = existingColumns[i].querySelector(".verb-cell");
      if (cell) {
        cell.className = "verb-cell"; // Remove hidden-cell class if it exists
        const value = currentVerb[columnHeaders[i]];
        cell.textContent = capitalizeFirstLetter(value);
      }
    }
  }
}

function updateStats() {
  totalQuestionsEl.textContent = totalQuestions;
  correctAnswersEl.textContent = correctAnswers;

  const percentage =
    totalQuestions > 0
      ? Math.round((correctAnswers / totalQuestions) * 100)
      : 0;
  percentageEl.textContent = percentage + "%";
}

function updateActionButton(text, className) {
  actionBtn.textContent = text;
  actionBtn.className = className;
}

function clearGameUI() {
  answerInput.value = "";
  feedback.style.display = "none";
  // Use setTimeout to ensure the input focus happens after the current event loop
  setTimeout(() => {
    answerInput.focus();
  }, 10);
}
