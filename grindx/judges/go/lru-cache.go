package main

import (
	"encoding/json"
	"math/rand"
)

// refLRU is a simple reference LRU implementation for verifying large cases.
type refLRU struct {
	cap   int
	order []int           // keys in access order, most recent at end
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
	}

	// Generate large TLE case: capacity=1000, 200K operations
	rng := rand.New(rand.NewSource(42))
	largeIdx := len(basicCases)

	capacity := 1000
	numOps := 200000

	cache := Constructor(capacity)
	ref := newRefLRU(capacity)

	for op := 0; op < numOps; op++ {
		if rng.Intn(3) != 0 {
			// ~67% put
			key := rng.Intn(5000)
			value := rng.Intn(100000)
			cache.Put(key, value)
			ref.put(key, value)
		} else {
			// ~33% get
			key := rng.Intn(5000)
			actual := cache.Get(key)
			expected := ref.get(key)
			if actual != expected {
				ReportWA(largeIdx, "large input (200K ops)", expected, actual, total, "tle")
			}
		}
	}

	ReportAC(total)
}
