// gameLogic.js - Core game logic and state management

// Game state
let verbs = [];
let currentVerb = null;
let columnHeaders = [];
let hiddenColumn = null;
let totalQuestions = 0;
let correctAnswers = 0;
let gameState = "waiting-for-answer"; // 'waiting-for-answer' or 'showing-feedback'

function loadVerbs() {
  // Get the selected file from sessionStorage
  const selectedFile = sessionStorage.getItem("selectedVerbFile");

  if (!selectedFile) {
    console.error("No verb file selected in the session storage.");
    document.getElementById("loading").textContent =
      "No verb file selected. Please go back to the main page and select a verb file.";
    return;
  }

  fetch(`Verbs/${selectedFile}`)
    .then((response) => response.text())
    .then((csvText) => {
      const csvBlob = new Blob([csvText], { type: "text/csv" });
      parseCSVFile(csvBlob, function (data, headers) {
        // Store the column headers for dynamic usage
        columnHeaders = headers;

        // Filter verbs to only include rows with all columns filled
        verbs = data.filter((verb) => {
          return columnHeaders.every(
            (header) => verb[header] && verb[header].trim() !== "",
          );
        });

        console.log("Loaded verbs:", verbs);
        console.log("Column headers:", columnHeaders);

        // Hide loading, show game
        document.getElementById("loading").style.display = "none";
        document.getElementById("game-area").style.display = "block";

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
  if (verbs.length === 0 || columnHeaders.length === 0) return;

  // Select random verb
  currentVerb = verbs[Math.floor(Math.random() * verbs.length)];

  // Select random column to hide (based on the number of available columns)
  hiddenColumn = Math.floor(Math.random() * columnHeaders.length);

  // Reset game state FIRST
  gameState = "waiting-for-answer";
  
  // Update UI
  updateActionButton("Check Answer", "action-btn check-btn");
  clearGameUI();
  displayVerb();
}

function checkAnswer() {
  if (!currentVerb) return;

  const userAnswer = document.getElementById("answer-input").value.trim().toLowerCase();
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
  gameState = "showing-feedback";
  updateActionButton("Next Verb", "action-btn next-btn");
  document.getElementById("answer-input").blur();
}

function getCorrectAnswer() {
  if (hiddenColumn >= 0 && hiddenColumn < columnHeaders.length) {
    return currentVerb[columnHeaders[hiddenColumn]];
  }
  return "";
}

function handleActionButton() {
  if (gameState === "waiting-for-answer") {
    checkAnswer();
  } else if (gameState === "showing-feedback") {
    nextVerb();
  }
}
