package main

import (
	"encoding/json"
)

// refLRU is a simple reference LRU implementation for verifying large cases.
type refLRU struct {
	cap   int
	order []int // keys in access order, most recent at end
	store map[int]int
}

func newRefLRU(capacity int) *refLRU {
	return &refLRU{cap: capacity, store: make(map[int]int)}
}

func (r *refLRU) touch(key int) {
	for i, k := range r.order {
		if k == key {
			r.order = append(r.order[:i], r.order[i+1:]...)
			break
		}
	}
	r.order = append(r.order, key)
}

func (r *refLRU) get(key int) int {
	if v, ok := r.store[key]; ok {
		r.touch(key)
		return v
	}
	return -1
}

func (r *refLRU) put(key, value int) {
	if _, ok := r.store[key]; ok {
		r.store[key] = value
		r.touch(key)
		return
	}
	if len(r.store) >= r.cap {
		lruKey := r.order[0]
		r.order = r.order[1:]
		delete(r.store, lruKey)
	}
	r.store[key] = value
	r.order = append(r.order, key)
}

func runLargeCase(total int, caseIdx int) {
	capacity := 3000
	totalOps := 200000
	cache := Constructor(capacity)
	ref := newRefLRU(capacity)

	for key := 0; key < capacity; key++ {
		value := (key * 97) % 100001
		cache.Put(key, value)
		ref.put(key, value)
	}

	for step := 0; step < totalOps-capacity; step++ {
		key := (step * 1879) % capacity
		if step%2 == 0 {
			actual := cache.Get(key)
			expected := ref.get(key)
			if actual != expected {
				ReportWA(caseIdx, "hidden input (adversarial 200K ops)", expected, actual, total, "stress")
			}
		} else {
			value := ((step * 7919) + key) % 100001
			cache.Put(key, value)
			ref.put(key, value)
		}
	}
}

func main() {
	tc := LoadCases("lru-cache")
	basicCases := tc.Cases

	total := len(basicCases) + 1

	// Run basic cases
	for i, c := range basicCases {
		var capacity int
		json.Unmarshal(c.Input[0], &capacity)

		cache := Constructor(capacity)

		var expectedAll []interface{}
		json.Unmarshal(c.Expected, &expectedAll)

		for j, op := range c.Operations {
			var args []int
			json.Unmarshal(c.OpInputs[j], &args)

			var result interface{}
			switch op {
			case "put":
				cache.Put(args[0], args[1])
				result = nil
			case "get":
				result = cache.Get(args[0])
			}

			// Only check non-null expected values
			if expectedAll[j] != nil {
				expectedVal := int(expectedAll[j].(float64))
				actualVal, ok := result.(int)
				if !ok || actualVal != expectedVal {
					ReportWA(i, c.Operations, expectedAll, result, total, c.Category)
				}
			}
		}
		ReportProgress(i + 1, total)
	}

	runLargeCase(total, len(basicCases))

	ReportAC(total)
}
