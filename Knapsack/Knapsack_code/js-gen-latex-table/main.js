const handlePrintRowLatex = require("./utils");
const fs = require("fs");

let beginTable =
  fs.readFileSync("./begin-table.txt", "utf8").split("\r").join("") + "\n";
let endTable =
  fs.readFileSync("./end-table.txt", "utf8").split("\r").join("") + "\n\n";

let fileContent = "",
  i = 0;
const idMx = 103;
for (let gr = 0; gr <= 12 && i < idMx; gr++) {
  fileContent += beginTable;
  for (let cnt = 0; i <= idMx && cnt < 8; cnt++, i++) {
    const ansFilename = `../output/Google-OR-Tools/test${i}.txt`;

    try {
      let data = fs.readFileSync(ansFilename, "utf8");
      fileContent += handlePrintRowLatex(data);
    } catch (err) {
      console.error(err);
    }
  }
  fileContent += endTable;
}

fs.writeFileSync("latex-table.txt", fileContent);
console.log(fileContent);
