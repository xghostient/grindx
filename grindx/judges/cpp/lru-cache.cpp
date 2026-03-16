/**
 * Judge for LRU Cache — design class pattern.
 */

#include "_common.h"
#include "solution.cpp"

#include <list>
#include <random>
#include <unordered_map>

// Reference LRU implementation for verifying large cases
class ReferenceLRU {
    int cap;
    std::list<std::pair<int, int>> order;
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> map;

public:
    ReferenceLRU(int capacity) : cap(capacity) {}

    int get(int key) {
        auto it = map.find(key);
        if (it == map.end()) return -1;
        order.splice(order.begin(), order, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = map.find(key);
        if (it != map.end()) {
            it->second->second = value;
            order.splice(order.begin(), order, it->second);
            return;
        }
        if (static_cast<int>(map.size()) >= cap) {
            auto& back = order.back();
            map.erase(back.first);
            order.pop_back();
        }
        order.push_front({key, value});
        map[key] = order.begin();
    }
};

int main() {
    auto tc = load_cases("lru-cache");
    auto& cases = tc["cases"].get_array();

    // Generate large case for TLE detection
    struct LargeOp {
        std::string op;
        int key;
        int value;
        int expected; // -2 means null (put returns nothing)
    };
    struct LargeCase {
        int capacity;
        std::vector<LargeOp> ops;
    };
    std::vector<LargeCase> large_cases;
    {
        int capacity = 1000;
        int num_ops = 200000;
        std::mt19937 rng(42);
        std::uniform_int_distribution<int> key_dist(1, 5000);
        std::uniform_int_distribution<int> val_dist(1, 100000);
        std::uniform_int_distribution<int> op_dist(0, 2); // bias toward put

        ReferenceLRU ref(capacity);
        std::vector<LargeOp> ops;

        for (int i = 0; i < num_ops; i++) {
            if (op_dist(rng) == 0) {
                // get
                int key = key_dist(rng);
                int expected = ref.get(key);
                ops.push_back({"get", key, 0, expected});
            } else {
                // put
                int key = key_dist(rng);
                int value = val_dist(rng);
                ref.put(key, value);
                ops.push_back({"put", key, value, -2});
            }
        }
        large_cases.push_back({capacity, ops});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        int capacity = c["input"][0].get<int>();
        auto& operations = c["operations"].get_array();
        auto& op_inputs = c["op_inputs"].get_array();
        auto& expected = c["expected"].get_array();

        LRUCache cache(capacity);

        for (int j = 0; j < static_cast<int>(operations.size()); j++) {
            const std::string& op = operations[j].get_string();
            if (op == "put") {
                int key = op_inputs[j][0].get<int>();
                int value = op_inputs[j][1].get<int>();
                cache.Put(key, value);
            } else if (op == "get") {
                int key = op_inputs[j][0].get<int>();
                int result = cache.Get(key);
                if (!expected[j].is_null()) {
                    int exp_val = expected[j].get<int>();
                    if (result != exp_val) {
                        std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
                        report_wa(i,
                            "op " + std::to_string(j) + ": get(" + std::to_string(key) + ")",
                            std::to_string(exp_val),
                            std::to_string(result),
                            total, cat);
                    }
                }
            }
        }
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];

        LRUCache cache(lc.capacity);

        for (int j = 0; j < static_cast<int>(lc.ops.size()); j++) {
            auto& op = lc.ops[j];
            if (op.op == "put") {
                cache.Put(op.key, op.value);
            } else {
                int result = cache.Get(op.key);
                if (result != op.expected) {
                    report_wa(idx,
                        "large input op " + std::to_string(j) + ": get(" + std::to_string(op.key) + ")",
                        std::to_string(op.expected),
                        std::to_string(result),
                        total, "tle");
                }
            }
        }
    }

    report_ac(total);
}
