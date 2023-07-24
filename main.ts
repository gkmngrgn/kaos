import * as d3 from "d3";
import { Rectangle2D, Point2D } from "./geometry";
import { generatePoints, ChaosGame } from './kaos';

async function createWorld(shape: Rectangle2D): Promise<d3.Selection<SVGSVGElement, unknown, HTMLElement, any>> {
  return d3.select("body")
    .append("svg")
    .attr("width", shape.width)
    .attr("height", shape.height);
}

async function drawPoints(world: d3.Selection<SVGSVGElement, unknown, HTMLElement, any>, points: Point2D[]) {
  world.selectAll()
    .data(points)
    .enter()
    .append("circle")
    .attr("cx", d => d.x)
    .attr("cy", d => d.y)
    .attr("r", 5)
    .attr("fill", "red");
}

async function main() {
  const world = await createWorld(new Rectangle2D(0, 0, 800, 800));
  let points = new Array(ChaosGame.maxIterations).fill(0).map(() => ({ x: 0, y: 0 }));
  let selection = 3;

  await generatePoints(points, selection);
  await drawPoints(world, points);
}

main();
