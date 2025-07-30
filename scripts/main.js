// main.js - Main initialization and page routing

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

// Game page initialization
function initializeGame() {
  initializeGameUI();
  loadVerbs();
}
