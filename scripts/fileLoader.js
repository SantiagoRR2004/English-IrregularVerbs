// fileLoader.js - Handles loading CSV files from local server or GitHub Pages

async function loadVerbFiles() {
  try {
    const currentUrl = window.location.href;
    const isGitHubPages = currentUrl.includes("github.io");

    let files = [];

    if (isGitHubPages) {
      files = await loadFromGitHubPages(currentUrl);
    } else {
      files = await loadFromLocalServer();
    }

    console.log("Found CSV files:", files);
    populateFileDropdown(files);
    restorePreviousSelection(files);
  } catch (error) {
    console.error("Error loading files:", error);
    showFileLoadError(error.message);
    throw error;
  }
}

async function loadFromGitHubPages(currentUrl) {
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
    throw new Error("Unable to parse GitHub Pages URL format: " + currentUrl);
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
  return data
    .filter((file) => file.name.endsWith(".csv"))
    .map((file) => file.name);
}

async function loadFromLocalServer() {
  // Local/Normal server: Try to discover CSV files dynamically
  console.log("Running on local server, attempting to discover CSV files");

  try {
    // Try to fetch the directory listing if the server supports it
    const dirResponse = await fetch("Verbs/");

    if (!dirResponse.ok) {
      throw new Error("Directory listing not available");
    }

    const dirText = await dirResponse.text();

    // Parse HTML directory listing for .csv files
    const parser = new DOMParser();
    const doc = parser.parseFromString(dirText, "text/html");
    const links = doc.querySelectorAll("a[href]");

    const files = [];
    for (const link of links) {
      const href = link.getAttribute("href");
      if (href && href.endsWith(".csv")) {
        files.push(href);
      }
    }

    console.log("Discovered files from directory listing:", files);

    if (files.length === 0) {
      throw new Error(
        "No CSV files could be discovered in the Verbs directory. Please ensure CSV files exist and are accessible.",
      );
    }

    return files;
  } catch (dirError) {
    console.log("Directory listing failed:", dirError.message);
    throw new Error(
      "No CSV files could be discovered in the Verbs directory. Please ensure CSV files exist and are accessible.",
    );
  }
}

function populateFileDropdown(files) {
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
}

function restorePreviousSelection(files) {
  const previouslySelected = sessionStorage.getItem("selectedVerbFile");
  if (previouslySelected && files.includes(previouslySelected)) {
    const select = document.getElementById("verb-file-select");
    select.value = previouslySelected;
  }
}

function showFileLoadError(message) {
  const select = document.getElementById("verb-file-select");
  select.innerHTML = `<option value="">Error: ${message}</option>`;
}
