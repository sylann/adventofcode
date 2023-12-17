package utils

import (
	"fmt"
	"os"
)

type ErrorHandler interface {
	Error(args ...any)
}

func ReadInputData(h ErrorHandler, inputRelPath string) string {
	bytes, err := os.ReadFile(fmt.Sprintf("../../../inputs/%s", inputRelPath))
	if err != nil {
		h.Error(err)
	}
	return string(bytes)
}
