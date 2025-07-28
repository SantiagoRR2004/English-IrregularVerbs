// scripts.js

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
        obj[header.trim()] = values[index].trim();
      });
      return obj;
    });

    callback(data); // Return parsed data
  };

  reader.readAsText(file);
}
