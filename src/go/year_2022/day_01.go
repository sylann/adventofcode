package year_2022

import (
	"container/heap"
	"fmt"
	"strconv"
	"strings"
)

type Day01 struct{}

func init() {
	Solutions[01] = Day01{}
}

type MaxHeap []int

// adapt from sort.IntSlice
func (h MaxHeap) Len() int           { return len(h) }
func (h MaxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h MaxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MaxHeap) Push(n any)        { *h = append(*h, n.(int)) }
func (h *MaxHeap) Pop() any {
	end := len(*h) - 1
	out := (*h)[end]
	*h = (*h)[0:end]
	return &out
}

func sumCaloriesOfNBest(data string, n int) int {
	h := make(MaxHeap, 0)
	heap.Init(&h)
	for _, elf := range strings.Split(data, "\n\n") {
		calories := 0
		for _, cal := range strings.Split(elf, "\n") {
			n, _ := strconv.Atoi(cal)
			calories += n
		}
		heap.Push(&h, calories)
	}

	out := 0
	for i := 0; i < n; i++ {
		out += *heap.Pop(&h).(*int)
	}
	return out
}

func (Day01) Solve1(data string) string {
	return fmt.Sprintf("%d", sumCaloriesOfNBest(data, 1))
}

func (Day01) Solve2(data string) string {
	return fmt.Sprintf("%d", sumCaloriesOfNBest(data, 3))
}
