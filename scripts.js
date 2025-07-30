// scripts.js

// Index page functions
async function loadVerbFiles() {
  try {
    const currentUrl = window.location.href;
    const isGitHubPages = currentUrl.includes("github.io");

    let files = [];

    if (isGitHubPages) {
      // GitHub Pages: Use GitHub API
      const urlParts = new URL(currentUrl);
      const pathParts = urlParts.pathname
        .split("/")
        .filter((part) => part.length > 0);

      let repoOwner, repoName;

      if (urlParts.hostname.includes("github.io")) {
        // Standard GitHub Pages: username.github.io/repo-name
        repoOwner = urlParts.hostname.split(".")[0];
        repoName = pathParts[0];
      } else {
        throw new Error(
          "Unable to parse GitHub Pages URL format: " + currentUrl,
        );
      }

      if (!repoOwner || !repoName) {
        throw new Error(
          "Could not extract repository information from URL: " + currentUrl,
        );
      }

      console.log(`Detected repository: ${repoOwner}/${repoName}`);

      // Use GitHub API to get files from the Verbs directory
      const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/Verbs`;
      console.log("Fetching from API:", apiUrl);

      const response = await fetch(apiUrl);

      if (!response.ok) {
        throw new Error(
          `GitHub API request failed: ${response.status} ${response.statusText}`,
        );
      }

      const data = await response.json();

      // Filter for CSV files
      files = data
        .filter((file) => file.name.endsWith(".csv"))
        .map((file) => file.name);
    } else {
      // Local/Normal server: Try to discover CSV files dynamically
      console.log("Running on local server, attempting to discover CSV files");

      try {
        // Try to fetch the directory listing if the server supports it
        const dirResponse = await fetch("Verbs/");

        if (dirResponse.ok) {
          const dirText = await dirResponse.text();

          // Parse HTML directory listing for .csv files
          const parser = new DOMParser();
          const doc = parser.parseFromString(dirText, "text/html");
          const links = doc.querySelectorAll("a[href]");

          for (const link of links) {
            const href = link.getAttribute("href");
            if (href && href.endsWith(".csv")) {
              files.push(href);
            }
          }

          console.log("Discovered files from directory listing:", files);
        } else {
          throw new Error("Directory listing not available");
        }
      } catch (dirError) {
        console.log("Directory listing failed:", dirError.message);

        throw new Error(
          "No CSV files could be discovered in the Verbs directory. Please ensure CSV files exist and are accessible.",
        );
      }
    }

    console.log("Found CSV files:", files);

    // Populate dropdown
    const select = document.getElementById("verb-file-select");
    select.innerHTML = '<option value="">Select a file...</option>';

    files.forEach((file) => {
      const option = document.createElement("option");
      option.value = file;
      option.textContent = file
        .replace(".csv", "")
        .replace(/([A-Z])/g, " $1")
        .trim();
      select.appendChild(option);
    });
  } catch (error) {
    console.error("Error loading files:", error);
    const select = document.getElementById("verb-file-select");
    select.innerHTML = `<option value="">Error: ${error.message}</option>`;
    throw error; // Re-throw to ensure the error is visible
  }
}

function initializeIndexPage() {
  // Load files when page loads
  loadVerbFiles();

  // Set up start game button event listener
  const startGameBtn = document.getElementById("start-game-btn");
  if (startGameBtn) {
    startGameBtn.addEventListener("click", function () {
      const selectedFile = document.getElementById("verb-file-select").value;
      if (selectedFile) {
        // Store the selected file in sessionStorage instead of URL parameter
        sessionStorage.setItem("selectedVerbFile", selectedFile);
        // Navigate to the game without any parameters
        window.location.href = "game.html";
      } else {
        alert("Please select a verb file first.");
      }
    });
  }
}

// Game state
let verbs = [];
let currentVerb = null;
let columnHeaders = []; // Store the CSV column headers dynamically
let hiddenColumn = null;
let totalQuestions = 0;
let correctAnswers = 0;
let gameState = "waiting-for-answer"; // 'waiting-for-answer' or 'showing-feedback'

// DOM elements
let gameArea, verbGrid, answerInput, feedback, actionBtn;
let totalQuestionsEl, correctAnswersEl, percentageEl;

// Initialize the appropriate page when the document loads
document.addEventListener("DOMContentLoaded", function () {
  // Check if we're on the index page or game page
  if (document.getElementById("verb-file-select")) {
    // We're on the index page
    initializeIndexPage();
  } else if (document.getElementById("game-area")) {
    // We're on the game page
    initializeGame();
  }
});

function parseCSVFile(file, callback) {
  const reader = new FileReader();

  reader.onload = function (event) {
    const text = event.target.result;
    const lines = text.trim().split("\n");
    const headers = lines[0].split(",").map((header) => header.trim());

    const data = lines.slice(1).map((line) => {
      const values = line.split(",");
      const obj = {};
      headers.forEach((header, index) => {
        obj[header] = values[index] ? values[index].trim() : "";
      });
      return obj;
    });

    callback(data, headers); // Return both parsed data and headers
  };

  reader.readAsText(file);
}

function initializeGame() {
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

  // Add document-level Enter key listener so it works even when input is not focused
  document.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      handleActionButton();
    }
  });

  // Load verbs data
  loadVerbs();
}

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
  if (verbs.length === 0 || columnHeaders.length === 0) return;

  // Select random verb
  currentVerb = verbs[Math.floor(Math.random() * verbs.length)];

  // Select random column to hide (based on the number of available columns)
  hiddenColumn = Math.floor(Math.random() * columnHeaders.length);

  // Reset game state
  gameState = "waiting-for-answer";
  actionBtn.textContent = "Check Answer";
  actionBtn.className = "action-btn check-btn";

  // Clear previous state
  answerInput.value = "";
  feedback.style.display = "none";
  answerInput.focus();

  // Display the verb with one column hidden
  displayVerb();
}

function handleActionButton() {
  if (gameState === "waiting-for-answer") {
    checkAnswer();
  } else if (gameState === "showing-feedback") {
    nextVerb();
  }
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
      // Capitalize the first letter of the verb value
      const capitalizedValue = value
        ? value.charAt(0).toUpperCase() + value.slice(1)
        : "";
      cell.textContent = capitalizedValue;
    }

    // Add header and cell to column
    column.appendChild(header);
    column.appendChild(cell);

    // Add column to grid
    verbGrid.appendChild(column);
  }
}

function checkAnswer() {
  if (!currentVerb) return;

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
  gameState = "showing-feedback";
  actionBtn.textContent = "Next Verb";
  actionBtn.className = "action-btn next-btn";
  answerInput.blur(); // Remove focus from input
}

function getCorrectAnswer() {
  if (hiddenColumn >= 0 && hiddenColumn < columnHeaders.length) {
    return currentVerb[columnHeaders[hiddenColumn]];
  }
  return "";
}

function showFeedback(isCorrect, correctAnswer) {
  feedback.style.display = "block";

  if (isCorrect) {
    feedback.className = "feedback correct";
    feedback.textContent = "Correct! Well done!";
  } else {
    feedback.className = "feedback incorrect";
    // Capitalize the first letter of the correct answer
    const capitalizedAnswer =
      correctAnswer.charAt(0).toUpperCase() + correctAnswer.slice(1);
    feedback.textContent = `Incorrect. The correct answer is: "${capitalizedAnswer}"`;
  }

  // Show the complete verb by updating the existing grid
  // Update the existing verb grid to show all answers
  const existingColumns = verbGrid.querySelectorAll(".verb-column");

  for (let i = 0; i < columnHeaders.length; i++) {
    if (existingColumns[i]) {
      const cell = existingColumns[i].querySelector(".verb-cell");
      if (cell) {
        cell.className = "verb-cell"; // Remove hidden-cell class if it exists
        // Get the value for this column
        const value = currentVerb[columnHeaders[i]];
        // Capitalize the first letter of the verb value
        const capitalizedValue = value
          ? value.charAt(0).toUpperCase() + value.slice(1)
          : "";
        cell.textContent = capitalizedValue;
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
