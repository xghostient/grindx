/**
 * Judge for LRU Cache — design class pattern.
 */

#include "_common.h"
#include "solution.cpp"

#include <list>
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
    int total = static_cast<int>(cases.size()) + 1;

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
        report_progress(i + 1, total);
    }

    {
        int idx = static_cast<int>(cases.size());
        int capacity = 3000;
        int total_ops = 200000;
        LRUCache cache(capacity);
        ReferenceLRU ref(capacity);

        for (int key = 0; key < capacity; key++) {
            int value = (key * 97) % 100001;
            cache.Put(key, value);
            ref.put(key, value);
        }

        for (int step = 0; step < total_ops - capacity; step++) {
            int key = (step * 1879) % capacity;
            if (step % 2 == 0) {
                int expected = ref.get(key);
                int result = cache.Get(key);
                if (result != expected) {
                    report_wa(
                        idx,
                        "stress op " + std::to_string(step) + ": get(" + std::to_string(key) + ")",
                        std::to_string(expected),
                        std::to_string(result),
                        total,
                        "stress"
                    );
                }
            } else {
                int value = ((step * 7919) + key) % 100001;
                cache.Put(key, value);
                ref.put(key, value);
            }
        }
    }

    report_ac(total);
}
