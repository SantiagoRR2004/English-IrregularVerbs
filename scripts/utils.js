// utils.js - Utility functions

// Function to handle back button navigation
function goBackToIndex() {
  // The selectedVerbFile is already stored in sessionStorage,
  // so we just need to navigate back to index.html
  window.location.href = "index.html";
}

// CSV parsing utility
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

// Utility to capitalize first letter
function capitalizeFirstLetter(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : "";
}
