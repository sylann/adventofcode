package utils

import (
	"flag"
	"fmt"
	_ "net/http/pprof"
	"os"
	"runtime"
	"runtime/pprof"
)

type profiler struct {
	doCpu, doMem bool
	cpuFile *os.File
}

// NewProfiler creates a new handle for easily starting cpu or heap profiles.
// It defines flags to control whether cpu and mem profiling are enabled.
// The `flag.Parse()` function must be called at some point after NewProfiler.
func NewProfiler() *profiler {
	p := profiler{}
	flag.BoolVar(&p.doCpu, "cpu", false, "write cpu profile to ./cpu.prof")
	flag.BoolVar(&p.doMem, "mem", false, "write mem profile to ./mem.prof")
	return &p
}

// StartCpuProfile creates a file at `./cpu.prof` (if cpu enabled) and then starts
// a CPU profile. Any error is printed immediately.
// You should always call `StopCpuProfile` after calling this function and the
// profiled code has finished executing (use defer in case of errors).
func (p *profiler) StartCpuProfile() {
	if !p.doCpu {
		return
	}
	var err error
	filename := "./cpu.prof"
	p.cpuFile, err = os.Create(filename)
	if err != nil {
		fmt.Printf("Failed creating file for CPU Profile: %v\n", err)
		return
	}
	fmt.Printf("Writing CPU Profile at: %v\n", filename)
	err = pprof.StartCPUProfile(p.cpuFile)
	if err != nil {
		fmt.Printf("Failed starting CPU profile: %v\n", err)
	} else {
		fmt.Print("Started CPU Profile\n")
	}
}

// MemProfile creates a file at `./mem.prof` (if mem enabled), writes a Heap
// profile to it and then closes the file. Any error is printed immediately.
func (p *profiler) MemProfile() {
	if !p.doMem {
		return
	}
	filename := "./mem.prof"
	f, err := os.Create(filename)
	if err != nil {
		fmt.Printf("Failed creating file for Heap Profile: %v\n", err)
		return
	}
	defer f.Close()
	fmt.Printf("Writing Heap Profile at: %v\n", filename)
	runtime.GC()
	err = pprof.WriteHeapProfile(f)
	if err != nil {
		fmt.Printf("Failed writing Heap Profile: %v\n", err)
	} else {
		fmt.Print("Heap Profile completed\n")
	}
}

// StopCpuProfile will cleanup dangling resources if needed.
// It should be called after `StartCpuProfile`.
// It has no effect if no resource need cleaning.
func (p *profiler) StopCpuProfile() {
	if p.cpuFile != nil {
		pprof.StopCPUProfile()
		p.cpuFile.Close()
		fmt.Print("Stopped CPU Profile\n")
	}
}
