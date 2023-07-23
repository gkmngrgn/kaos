import * as d3 from "d3";
import { Rectangle2D, Point2D } from "./geometry";

const width = 800;
const height = 800;

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
  const screenSpace = new Rectangle2D(0, 0, width - 1, height - 1);
  const points: Point2D[] = new Array(width / 20).fill(0).map((_, i) => ({ x: i * 20, y: height - i * 20 }));
  await drawPoints(world, points);
  // Rectangle2D screen_space{0, static_cast<double>(height - 1), static_cast<double>(width - 1), 0};
  // backend_sdl2(int width, int height, const Rectangle2D &world, const Rectangle2D &screen_space, int point_radius)
  // backend_sdl2(width, height, world, screen_space, points, 5);
}

main();
