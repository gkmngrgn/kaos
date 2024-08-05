package main

import (
	"fmt"
	"os"
	"strconv"
)

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
	// TODO: not ready yet.
	fmt.Printf("Saving to: %s\n", file_name)
}
