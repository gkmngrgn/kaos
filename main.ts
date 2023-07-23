import * as d3 from "d3";

const width = 800;
const height = 800;

async function demo() {
  var svg = d3.select("body")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  var data = [{ x1: 20, x2: 60, y1: 30, y2: 50 },
  { x1: 50, x2: 80, y1: 100, y2: 200 },
  { x1: 200, x2: 400, y1: 10, y2: 100 }];

  svg.selectAll("foo")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", d => d.x1)
    .attr("y", d => d.y1)
    .attr("width", d => d.x2 - d.x1)
    .attr("height", d => d.y2 - d.y1)
    .attr("fill", "teal");
}

async function main() {
  await demo();
}

main();
