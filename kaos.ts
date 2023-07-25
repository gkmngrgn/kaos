import { Point2D, RegularPolygon } from "./geometry";


export class ChaosGame {
    static readonly maxIterations = 100000;
    static readonly ignoreFirstIterations = 10;

    lastPoint: Point2D;
    lastVertex: number;

    constructor(
        public polygon: RegularPolygon
    ) {
        this.lastPoint = polygon.points[0];
        this.lastVertex = 0;
    }

    getNextPoint(func: (randomVertex: number, lastVertex: number, dist: number) => boolean, ratio = 0.5, dist = 0) {
        let running = true;
        let removeIter = 0;

        while (running) {
            const randomVertex = Math.floor(Math.random() * this.polygon.nrEdges);

            if (func(randomVertex, this.lastVertex, dist)) {
                const point = {
                    x: (this.lastPoint.x + this.polygon.points[randomVertex].x) * ratio,
                    y: (this.lastPoint.y + this.polygon.points[randomVertex].y) * ratio,
                };

                this.lastVertex = randomVertex;
                this.lastPoint = point;
                removeIter++;

                if (removeIter >= ChaosGame.ignoreFirstIterations) {
                    running = false;
                }
            }
        }

        return this.lastPoint;
    }
}

export async function generatePoints(points: Point2D[], selection = 0): Promise<number> {
    // wrap the values for selection values larger than the number of implemented selections
    if (selection > 14) {
        selection = 0;
    }

    let nrEdges, ratio, distance, func;

    if (selection === 1) {
        nrEdges = 4;
        ratio = 0.5;
        distance = 0;
        func = (randomVertex: number, lastVertex: number, dist: number) => Math.abs(randomVertex - lastVertex) !== dist;
    } else {
        nrEdges = 3;
        ratio = 0.5;
        distance = 0;
        func = () => true;
    }

    const polygon = new RegularPolygon(nrEdges);
    const chaos = new ChaosGame(polygon);

    for (const p of points) {
        const nextPoint = chaos.getNextPoint(func, ratio, distance);
        p.x = nextPoint.x;
        p.y = nextPoint.y;
    }

    return selection;
}
