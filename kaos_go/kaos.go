package main

import (
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"math"
	"math/rand"
	"os"
	"strconv"

	"golang.org/x/image/bmp"
)

const (
	WIDTH          = 800
	HEIGHT         = 800
	MAX_ITERATIONS = 100000
)

type Point2D struct {
	X, Y float64
}

type Rectangle2D struct {
	Left, Bottom, Right, Top float64
}

type RegularPolygon struct {
	NrEdges    int
	Radius     float64
	StartAngle float64
	Angle      float64
	Points     []Point2D
}

func NewRegularPolygon(nrEdges int, radius float64, startAngle float64) *RegularPolygon {
	angle := 360.0 / float64(nrEdges)

	// We change the start_angle in order to have the lower edge of every polygon parallel with the horizontal axis.
	if nrEdges%2 == 0 {
		startAngle += angle / 2.0
	}

	rp := &RegularPolygon{
		NrEdges:    nrEdges,
		Radius:     radius,
		StartAngle: startAngle,
		Angle:      angle,
	}
	rp.initPoints()
	return rp
}

func (rp *RegularPolygon) initPoints() {
	degRad := math.Pi / 180.0
	currentAngle := rp.StartAngle * degRad
	minY := 2.0

	for index := 0; index < rp.NrEdges; index++ {
		point := Point2D{
			X: rp.Radius * math.Cos(currentAngle),
			Y: rp.Radius * math.Sin(currentAngle),
		}
		rp.Points = append(rp.Points, point)

		if minY > point.Y {
			minY = point.Y
		}

		currentAngle += rp.Angle * degRad
	}
}

type KaosGame struct {
	Polygon               RegularPolygon
	LastPoint             Point2D
	LastVertex            int
	MaxIterations         int
	IgnoreFirstIterations int
}

func NewKaosGame(polygon RegularPolygon) *KaosGame {
	return &KaosGame{
		Polygon:               polygon,
		LastPoint:             polygon.Points[0],
		LastVertex:            0,
		MaxIterations:         MAX_ITERATIONS,
		IgnoreFirstIterations: 10,
	}
}

func (kg *KaosGame) GetNextPoint(
	fn func(int, int, int) bool,
	ratio float64,
	dist int,
) Point2D {
	running := true
	removeIter := 0

	for running {
		randomVertex := rand.Intn(len(kg.Polygon.Points))

		if fn(randomVertex, kg.LastVertex, dist) {
			randomPoint := kg.Polygon.Points[randomVertex]
			point := Point2D{
				X: (kg.LastPoint.X + randomPoint.X) * ratio,
				Y: (kg.LastPoint.Y + randomPoint.Y) * ratio,
			}
			kg.LastVertex = randomVertex
			kg.LastPoint = point
			removeIter++

			if removeIter >= kg.IgnoreFirstIterations {
				running = false
			}
		}
	}

	return kg.LastPoint
}

type WorldToScreenSpace struct {
	A, B, C, D float64
}

func NewWorldToScreenSpace(world, screenSpace Rectangle2D) *WorldToScreenSpace {
	a := (screenSpace.Right - screenSpace.Left) / (world.Right - world.Left)
	b := (screenSpace.Top - screenSpace.Bottom) / (world.Top - world.Bottom)
	c := screenSpace.Left - a*world.Left
	d := screenSpace.Bottom - c*world.Bottom
	return &WorldToScreenSpace{A: a, B: b, C: c, D: d}
}

func (w2ss *WorldToScreenSpace) Mapping(point Point2D) Point2D {
	x := w2ss.A*point.X + w2ss.C
	y := w2ss.B*point.Y + w2ss.D
	return Point2D{X: x, Y: y}
}

func isPointValid(randomVertex, lastVertex, dist int) bool {
	return math.Abs(float64(randomVertex-lastVertex)) != float64(dist)
}

func isPointValid1(randomVertex, lastVertex, dist int) bool {
	return true
}

func generate_points(maxIterations int, selection int) []Point2D {
	var points []Point2D
	var isValidFn func(int, int, int) bool
	var nrEdges int
	var ratio float64
	var distance int

	switch selection {
	case 1:
		isValidFn = isPointValid
		nrEdges = 4
		ratio = 0.5
		distance = 0
	case 2:
		isValidFn = isPointValid
		nrEdges = 4
		ratio = 0.5
		distance = 2
	case 3:
		isValidFn = isPointValid
		nrEdges = 5
		ratio = 0.5
		distance = 0
	case 4:
		isValidFn = isPointValid1
		nrEdges = 7
		ratio = 0.4
		distance = 0
	case 5:
		isValidFn = isPointValid
		nrEdges = 7
		ratio = 0.4
		distance = 3
	case 6:
		isValidFn = isPointValid
		nrEdges = 6
		ratio = 0.4
		distance = 3
	case 7:
		isValidFn = isPointValid
		nrEdges = 6
		ratio = 0.375
		distance = 0
	case 8:
		isValidFn = isPointValid
		nrEdges = 6
		ratio = 0.5
		distance = 2
	case 9:
		isValidFn = isPointValid
		nrEdges = 8
		ratio = 0.4
		distance = 0
	case 10:
		isValidFn = isPointValid
		nrEdges = 10
		ratio = 0.375
		distance = 1
	case 11:
		isValidFn = isPointValid
		nrEdges = 10
		ratio = 0.375
		distance = 2
	case 12:
		isValidFn = isPointValid
		nrEdges = 10
		ratio = 0.375
		distance = 3
	case 13:
		isValidFn = isPointValid
		nrEdges = 10
		ratio = 0.375
		distance = 4
	case 14:
		isValidFn = isPointValid
		nrEdges = 10
		ratio = 0.375
		distance = 5
	default:
		isValidFn = isPointValid1
		nrEdges = 3
		ratio = 0.5
		distance = 0
	}

	polygon := NewRegularPolygon(nrEdges, 1.0, 90.0)
	kaos := NewKaosGame(*polygon)

	for i := 0; i < maxIterations; i++ {
		point := kaos.GetNextPoint(isValidFn, ratio, distance)
		points = append(points, point)
	}

	return points
}

func pointsToScreenSpace(world, screenSpace Rectangle2D, points []Point2D) []Point2D {
	w2ss := NewWorldToScreenSpace(world, screenSpace)
	var screenPoints []Point2D
	for _, p := range points {
		screenPoints = append(screenPoints, w2ss.Mapping(p))
	}
	return screenPoints
}

func backendBmp(
	fileName string,
	width, height int,
	world, screenSpace Rectangle2D,
	points []Point2D,
	pointRadius int,
) {
	points = pointsToScreenSpace(world, screenSpace, points)
	img := image.NewRGBA(image.Rect(0, 0, width, height))
	bgColor := color.RGBA{255, 255, 255, 255}
	draw.Draw(img, img.Bounds(), &image.Uniform{bgColor}, image.Point{}, draw.Src)
	pointColor := color.RGBA{255, 0, 0, 255}
	radius2 := pointRadius * pointRadius

	if pointRadius == 0 {
		for _, point := range points {
			img.Set(int(point.X), int(point.Y), pointColor)
		}
	} else {
		for _, point := range points {
			xmin := int(math.Max(point.X-float64(pointRadius), 0))
			xmax := int(math.Min(point.X+float64(pointRadius), float64(width-1)))
			ymin := int(math.Max(point.Y-float64(pointRadius), 0))
			ymax := int(math.Min(point.Y+float64(pointRadius), float64(height-1)))

			for j := ymin; j <= ymax; j++ {
				for i := xmin; i <= xmax; i++ {
					dist := (i-int(point.X))*(i-int(point.X)) + (j-int(point.Y))*(j-int(point.Y))
					if dist <= radius2 {
						img.Set(i, j, pointColor)
					}
				}
			}
		}
	}

	outFile, err := os.Create(fileName)
	if err != nil {
		panic(err)
	}
	defer outFile.Close()

	err = bmp.Encode(outFile, img)
	if err != nil {
		panic(err)
	}
}

func main() {
	var selection int

	if len(os.Args) > 1 {
		num, err := strconv.Atoi(os.Args[1])
		if err != nil {
			selection = 0
		} else {
			selection = num
		}
	} else {
		selection = 0
	}

	fmt.Printf("Selection is: %d\n", selection)
	world := Rectangle2D{Left: -1.08, Bottom: -1.08, Right: 1.08, Top: 1.08}
	points := generate_points(MAX_ITERATIONS, selection)
	screenSpace := Rectangle2D{Left: 0, Bottom: 0, Right: WIDTH - 1, Top: HEIGHT - 1}
	fileName := fmt.Sprintf("kaos_%d.bmp", selection)
	backendBmp(fileName, WIDTH, HEIGHT, world, screenSpace, points, 0)
	fmt.Printf("Saved to: %s\n", fileName)
}
