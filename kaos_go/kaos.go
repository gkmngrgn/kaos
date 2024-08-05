package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
)

const (
	WIDTH  = 800
	HEIGHT = 800
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
	Points     [][]float64
}

func NewRegularPolygon(nrEdges int, radius float64, startAngle float64) *RegularPolygon {
	rp := &RegularPolygon{
		NrEdges:    nrEdges,
		Radius:     radius,
		StartAngle: startAngle,
	}
	rp.Angle = 360.0 / float64(nrEdges)
	rp.Points = make([][]float64, nrEdges)
	for i := range rp.Points {
		rp.Points[i] = make([]float64, 2)
	}

	if nrEdges%2 == 0 {
		rp.StartAngle += rp.Angle / 2.0
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

		rp.Points[index][0] = point.X
		rp.Points[index][1] = point.Y

		if minY > point.Y {
			minY = point.Y
		}

		currentAngle += rp.Angle * degRad
	}
}

func generate_points(max_iterations int, selection int) []Point2D {
	var points []Point2D
	var nrEdges int

	switch selection {
	case 1:
		// func = is_valid_point
		nrEdges = 4
		// ratio = 0.5
		// distance = 0
	case 2:
		// func = is_valid_point
		nrEdges = 4
		// ratio = 0.5
		// distance = 2
	case 3:
		// func = is_valid_point
		nrEdges = 5
		// ratio = 0.5
		// distance = 0

	case 4:
		// func = is_valid_point_1
		nrEdges = 7
		// ratio = 0.4
		// distance = 0

	case 5:
		// func = is_valid_point
		nrEdges = 7
		// ratio = 0.4
		// distance = 3

	case 6:
		// func = is_valid_point
		nrEdges = 6
		// ratio = 0.4
		// distance = 3

	case 7:
		// func = is_valid_point
		nrEdges = 6
		// ratio = 0.375
		// distance = 0

	case 8:
		// func = is_valid_point
		nrEdges = 6
		// ratio = 0.5
		// distance = 2

	case 9:
		// func = is_valid_point
		nrEdges = 8
		// ratio = 0.4
		// distance = 0

	case 10:
		// func = is_valid_point
		nrEdges = 10
		// ratio = 0.375
		// distance = 1

	case 11:
		// func = is_valid_point
		nrEdges = 10
		// ratio = 0.375
		// distance = 2

	case 12:
		// func = is_valid_point
		nrEdges = 10
		// ratio = 0.375
		// distance = 3

	case 13:
		// func = is_valid_point
		nrEdges = 10
		// ratio = 0.375
		// distance = 4

	case 14:
		// func = is_valid_point
		nrEdges = 10
		// ratio = 0.375
		// distance = 5

	default:
		// func = is_valid_point_1
		nrEdges = 3
		// ratio = 0.5
		// distance = 0
	}

	polygon := NewRegularPolygon(nrEdges, 1.0, 90.0)
	return points
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

	file_name := fmt.Sprintf("kaos_%d.bmp", selection)
	// points = generate_points(KaosGame.max_iterations, selection=selection)
	fmt.Printf("Saving to: %s\n", file_name)
}
