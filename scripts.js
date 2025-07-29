// scripts.js

// Game state
let verbs = [];
let currentVerb = null;
let hiddenColumn = null;
let totalQuestions = 0;
let correctAnswers = 0;
let gameState = 'waiting-for-answer'; // 'waiting-for-answer' or 'showing-feedback'

// DOM elements
let gameArea, verbRow, answerInput, feedback, actionBtn;
let totalQuestionsEl, correctAnswersEl, percentageEl;

// Initialize the game when the page loads
document.addEventListener("DOMContentLoaded", function () {
  initializeGame();
});

export function parseCSVFile(file, callback) {
  const reader = new FileReader();

  reader.onload = function (event) {
    const text = event.target.result;
    const lines = text.trim().split("\n");
    const headers = lines[0].split("\t");

    const data = lines.slice(1).map((line) => {
      const values = line.split("\t");
      const obj = {};
      headers.forEach((header, index) => {
        obj[header.trim()] = values[index] ? values[index].trim() : "";
      });
      return obj;
    });

    callback(data); // Return parsed data
  };

  reader.readAsText(file);
}

function initializeGame() {
  // Get DOM elements
  gameArea = document.getElementById("game-area");
  verbRow = document.getElementById("verb-row");
  answerInput = document.getElementById("answer-input");
  feedback = document.getElementById("feedback");
  actionBtn = document.getElementById("action-btn");
  totalQuestionsEl = document.getElementById("total-questions");
  correctAnswersEl = document.getElementById("correct-answers");
  percentageEl = document.getElementById("percentage");

  // Set up event listeners
  actionBtn.addEventListener("click", handleActionButton);
  answerInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
    handleActionButton();
    }
  });

  // Load verbs data
  loadVerbs();
}

function loadVerbs() {
  fetch("Verbs/ListaVerbos.txt")
    .then((response) => response.text())
    .then((csvText) => {
      const csvBlob = new Blob([csvText], { type: "text/csv" });
      parseCSVFile(csvBlob, function (data) {
        verbs = data.filter(
          (verb) =>
            verb.Infinitive &&
            verb["Past Simple"] &&
            verb["Past participle"] &&
            verb.Significado,
        );
        console.log("Loaded verbs:", verbs);

        // Hide loading, show game
        document.getElementById("loading").style.display = "none";
        gameArea.style.display = "block";

        // Start the first question
        nextVerb();
      });
    })
    .catch((err) => {
      console.error("Failed to load verbs file:", err);
      document.getElementById("loading").textContent =
        "Error loading verbs file.";
    });
}

function nextVerb() {
  if (verbs.length === 0) return;

  // Select random verb
  currentVerb = verbs[Math.floor(Math.random() * verbs.length)];

  // Select random column to hide (0: Infinitive, 1: Past Simple, 2: Past Participle, 3: Meaning)
  hiddenColumn = Math.floor(Math.random() * 4);

  // Reset game state
  gameState = 'waiting-for-answer';
  actionBtn.textContent =  'Check Answer';
  actionBtn.className = 'action-btn check-btn';

  // Clear previous state
  answerInput.value = "";
  feedback.style.display = "none";
  answerInput.focus();

  // Display the verb with one column hidden
  displayVerb();
}

function handleActionButton() {
  if (gameState === 'waiting-for-answer') {
    checkAnswer();
  } else if (gameState === 'showing-feedback') {
    nextVerb();
  }
}

function displayVerb() {
  const columns = [
    "Infinitive",
    "Past Simple",
    "Past participle",
    "Significado",
  ];
  const values = [
    currentVerb.Infinitive,
    currentVerb["Past Simple"],
    currentVerb["Past participle"],
    currentVerb.Significado,
  ];

  verbRow.innerHTML = "";

  for (let i = 0; i < 4; i++) {
    const cell = document.createElement("div");
    cell.className = "verb-cell";

    if (i === hiddenColumn) {
      cell.className += " hidden-cell";
      cell.textContent = "???";
    } else {
      cell.textContent = values[i];
    }

    verbRow.appendChild(cell);
  }
}

function checkAnswer() {
  if (!currentVerb || answerInput.value.trim() === "") return;

  const userAnswer = answerInput.value.trim().toLowerCase();
  const correctAnswer = getCorrectAnswer().toLowerCase();

  totalQuestions++;

  if (userAnswer === correctAnswer) {
    correctAnswers++;
    showFeedback(true, correctAnswer);
  } else {
    showFeedback(false, correctAnswer);
  }

  updateStats();
  
  // Change button to "Next Verb"
  gameState = 'showing-feedback';
  actionBtn.textContent = 'Next Verb';
  actionBtn.className = 'action-btn next-btn';
  answerInput.blur();  // Remove focus from input
}

function getCorrectAnswer() {
  switch (hiddenColumn) {
    case 0:
      return currentVerb.Infinitive;
    case 1:
      return currentVerb["Past Simple"];
    case 2:
      return currentVerb["Past participle"];
    case 3:
      return currentVerb.Significado;
    default:
      return "";
  }
}

function showFeedback(isCorrect, correctAnswer) {
  feedback.style.display = "block";

  if (isCorrect) {
    feedback.className = "feedback correct";
    feedback.textContent = "Correct! Well done!";
  } else {
    feedback.className = "feedback incorrect";
    feedback.textContent = `Incorrect. The correct answer is: "${correctAnswer}"`;
  }

  // Show the complete verb
  const columns = [
    "Infinitive",
    "Past Simple",
    "Past participle",
    "Significado",
  ];
  const values = [
    currentVerb.Infinitive,
    currentVerb["Past Simple"],
    currentVerb["Past participle"],
    currentVerb.Significado,
  ];

  verbRow.innerHTML = "";

  for (let i = 0; i < 4; i++) {
    const cell = document.createElement("div");
    cell.className = "verb-cell";
    cell.textContent = values[i];
    verbRow.appendChild(cell);
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
