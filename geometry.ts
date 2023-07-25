export interface Point2D {
  x: number;
  y: number;
}

export class Rectangle2D {
  constructor(
    public left: number,
    public bottom: number,
    public right: number,
    public top: number
  ) { }

  get width(): number {
    return this.right - this.left;
  }

  get height(): number {
    return this.top - this.bottom;
  }
}

export class RegularPolygon {
  readonly degRad = Math.PI / 180.0;
  angle: number;
  startAngle = 90.0;
  points: Point2D[];

  constructor(
    public nrEdges: number = 3,
    public radius: number = 1.0,
  ) {
    this.angle = 360.0 / this.nrEdges;

    // we change the startAngle in order to have the lower edge of every polygon
    // parallel with the horizontal axis.
    if (this.nrEdges % 2 === 0) {
      this.startAngle += this.angle / 2.0;
    }

    this.points = new Array(this.nrEdges);
    this.initPoints();
  }

  initPoints() {
    let currentAngle = this.startAngle * this.degRad;
    let minY = 2.0;

    for (let i = 0; i < this.nrEdges; ++i) {
      this.points[i] = {
        x: this.radius * Math.cos(currentAngle),
        y: this.radius * Math.sin(currentAngle),
      };

      if (minY > this.points[i].y) {
        minY = this.points[i].y;
      }

      currentAngle += this.angle * this.degRad;
    }

    // center the points vertically
    const offset = (2.0 - (1.0 - minY)) / 2.0;

    if (this.nrEdges % 2 !== 0) {
      for (let i = 0; i < this.nrEdges; ++i) {
        this.points[i].y -= offset;
      }
    }
  }
}
