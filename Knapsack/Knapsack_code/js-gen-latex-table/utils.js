let stt = 1;

function handlePrintRowLatex(data) {
  data = data.split("\n");
  // console.log(data);

  let filename = String(data[0]).split(": ")[1].substring(5);
  filename = filename.split("\r")[0];
  let tmp = filename.split("/");
  filename = tmp[0].substring(0, 2);
  tmp = tmp.splice(1).join("/");
  filename += "/" + tmp;

  let N = Number(filename.split("/")[1].split("n")[1]);
  // console.log(N);

  let capaticy = String(data[2]).split(" = ")[1].split("\r")[0];
  // console.log(capaticy);

  let totalWeight = Number(String(data[3]).split(" = ")[1].split("\r")[0]);
  // console.log(totalWeight);

  let totalValue = String(data[4]).split(" = ")[1].split("\r")[0];
  // console.log(totalValue);

  const cur = `${stt} & ${filename} & ${N} & ${capaticy} & ${totalWeight} & ${totalValue} \\\\\n`;
  stt++;
  return cur;
}

module.exports = handlePrintRowLatex;
