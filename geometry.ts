interface Point2D {
  x: number;
  y: number;
}

interface Rectangle2D {
  left: number;
  bottom: number;
  right: number;
  top: number;
}

function createRectangle2D(left: number, bottom: number, right: number, top: number): Rectangle2D {
  return { left, bottom, right, top };
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
