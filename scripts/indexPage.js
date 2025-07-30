// indexPage.js - Index page initialization and event handling

function initializeIndexPage() {
  // Load files when page loads
  loadVerbFiles();

  // Set up start game button event listener
  const startGameBtn = document.getElementById("start-game-btn");
  if (startGameBtn) {
    startGameBtn.addEventListener("click", handleStartGame);
  }
}

function handleStartGame() {
  const selectedFile = document.getElementById("verb-file-select").value;
  if (selectedFile) {
    // Store the selected file in sessionStorage instead of URL parameter
    sessionStorage.setItem("selectedVerbFile", selectedFile);
    // Navigate to the game without any parameters
    window.location.href = "game.html";
  } else {
    alert("Please select a verb file first.");
  }
}
