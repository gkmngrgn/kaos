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

class WorldToScreenSpace {
  A: number;
  B: number;
  C: number;
  D: number;

  constructor(world: Rectangle2D, screenSpace: Rectangle2D) {
    this.A = (screenSpace.right - screenSpace.left) / (world.right - world.left);
    this.B = (screenSpace.top - screenSpace.bottom) / (world.top - world.bottom);
    this.C = screenSpace.left - this.A * world.left;
    this.D = screenSpace.bottom - this.B * world.bottom;
  }

  mapping(point: Point2D): Point2D {
    return {
      x: this.A * point.x + this.C,
      y: this.B * point.y + this.D
    };
  }
}
