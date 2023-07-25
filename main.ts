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
  const worldCenter: Point2D = {
    x: parseInt(world.attr("width")) / 2,
    y: parseInt(world.attr("height")) / 2
  };
  world.selectAll()
    .data(points)
    .enter()
    .append("circle")
    .attr("cx", d => worldCenter.x - Math.round(d.x * worldCenter.x))
    .attr("cy", d => worldCenter.y - Math.round(d.y * worldCenter.y))
    .attr("r", 0.5)
    .attr("fill", "red")
    .attr('opacity', 0)
    .transition()
    .duration(0.25)
    .delay((d, i) => i * 0.25)
    .attr('opacity', 1);;
}

async function main() {
  const world = await createWorld(new Rectangle2D(0, 0, 500, 500));
  let points = new Array(ChaosGame.maxIterations).fill(0).map(() => ({ x: 0, y: 0 }));

  await generatePoints(points, 2);
  await drawPoints(world, points);
}

main();
