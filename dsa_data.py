"""
dsa_data.py
Comprehensive offline dataset of Data Structures and Algorithms questions.
Includes all 14 requested topics across Easy, Medium, and Hard difficulty levels.
Each question includes problem statements, examples, hints, explanations, starter code,
standard solution, and automated test cases for safe evaluation.
"""

DSA_TOPICS = [
    "Arrays",
    "Strings",
    "Linked Lists",
    "Stacks",
    "Queues",
    "Hashing",
    "Recursion",
    "Sorting",
    "Searching",
    "Trees",
    "Binary Search Trees",
    "Heaps",
    "Graphs",
    "Dynamic Programming"
]

DSA_DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Master dataset of questions
DSA_QUESTIONS = [
    # --- ARRAYS ---
    {
        "id": "arr_01",
        "title": "Two Sum",
        "topic": "Arrays",
        "difficulty": "Easy",
        "statement": "Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "examples": [
            {"input": "nums = [2, 7, 11, 15], target = 9", "output": "[0, 1]", "explanation": "nums[0] + nums[1] == 9, so return [0, 1]."},
            {"input": "nums = [3, 2, 4], target = 6", "output": "[1, 2]", "explanation": "nums[1] + nums[2] == 6, so return [1, 2]."}
        ],
        "hints": [
            "A brute force approach checks all pairs in O(n^2). Can you do it in O(n)?",
            "Think about what value you need to find when at `num`: `target - num`. Can a hash table store seen numbers?"
        ],
        "approach": "Hash Map (One-Pass). Iterate through the list while maintaining a dictionary mapping number to index. If `target - num` exists in the dictionary, return the current index and stored index.",
        "starter_code": "def two_sum(nums, target):\n    # Write your solution here\n    # Return a list of two indices [idx1, idx2]\n    pass\n",
        "solution": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n",
        "test_cases": [
            {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"args": [[3, 2, 4], 6], "expected": [1, 2]},
            {"args": [[3, 3], 6], "expected": [0, 1]}
        ]
    },
    {
        "id": "arr_02",
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "topic": "Arrays",
        "difficulty": "Medium",
        "statement": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "examples": [
            {"input": "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]", "output": "6", "explanation": "The subarray [4, -1, 2, 1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1", "explanation": "Single element array."}
        ],
        "hints": [
            "As you iterate, either add the current number to the current running subarray, or start a fresh subarray at the current number.",
            "If current sum becomes negative, reset it to the current element."
        ],
        "approach": "Kadane's Algorithm: Maintain `current_sum` and `max_sum`. Update `current_sum = max(num, current_sum + num)` and `max_sum = max(max_sum, current_sum)`.",
        "starter_code": "def max_sub_array(nums):\n    # Write your solution here\n    # Return the maximum subarray sum (int)\n    pass\n",
        "solution": "def max_sub_array(nums):\n    if not nums:\n        return 0\n    max_sum = current_sum = nums[0]\n    for num in nums[1:]:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum\n",
        "test_cases": [
            {"args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6},
            {"args": [[1]], "expected": 1},
            {"args": [[5, 4, -1, 7, 8]], "expected": 23}
        ]
    },
    {
        "id": "arr_03",
        "title": "Trapping Rain Water",
        "topic": "Arrays",
        "difficulty": "Hard",
        "statement": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of rain water are trapped."},
            {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units of rain water are trapped."}
        ],
        "hints": [
            "For each element, water trapped depends on the minimum of max height to its left and max height to its right.",
            "Can you use two pointers from both ends to solve this in O(1) extra space?"
        ],
        "approach": "Two Pointers. Move the pointer on the side with the smaller max boundary inwards, accumulating water whenever the current bar is lower than that boundary.",
        "starter_code": "def trap_rain_water(height):\n    # Write your solution here\n    # Return total trapped water (int)\n    pass\n",
        "solution": "def trap_rain_water(height):\n    if not height:\n        return 0\n    left, right = 0, len(height) - 1\n    left_max, right_max = height[left], height[right]\n    trapped = 0\n    while left < right:\n        if left_max < right_max:\n            left += 1\n            left_max = max(left_max, height[left])\n            trapped += left_max - height[left]\n        else:\n            right -= 1\n            right_max = max(right_max, height[right])\n            trapped += right_max - height[right]\n    return trapped\n",
        "test_cases": [
            {"args": [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], "expected": 6},
            {"args": [[4, 2, 0, 3, 2, 5]], "expected": 9}
        ]
    },

    # --- STRINGS ---
    {
        "id": "str_01",
        "title": "Valid Palindrome",
        "topic": "Strings",
        "difficulty": "Easy",
        "statement": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Return `True` if palindrome, else `False`.",
        "examples": [
            {"input": "s = 'A man, a plan, a canal: Panama'", "output": "True", "explanation": "'amanaplanacanalpanama' is a palindrome."},
            {"input": "s = 'race a car'", "output": "False", "explanation": "'raceacar' is not a palindrome."}
        ],
        "hints": [
            "Filter alphanumeric characters and lowercase them first.",
            "Alternatively, use two pointers skipping non-alphanumeric characters."
        ],
        "approach": "Two-pointer check or filtered string comparison `filtered == filtered[::-1]`.",
        "starter_code": "def is_palindrome(s):\n    # Write your solution here\n    # Return boolean\n    pass\n",
        "solution": "def is_palindrome(s):\n    filtered = [ch.lower() for ch in s if ch.isalnum()]\n    return filtered == filtered[::-1]\n",
        "test_cases": [
            {"args": ["A man, a plan, a canal: Panama"], "expected": True},
            {"args": ["race a car"], "expected": False},
            {"args": [" "], "expected": True}
        ]
    },
    {
        "id": "str_02",
        "title": "Longest Substring Without Repeating Characters",
        "topic": "Strings",
        "difficulty": "Medium",
        "statement": "Given a string `s`, find the length of the longest substring without duplicate characters.",
        "examples": [
            {"input": "s = 'abcabcbb'", "output": "3", "explanation": "The answer is 'abc', with length 3."},
            {"input": "s = 'bbbbb'", "output": "1", "explanation": "The answer is 'b', with length 1."}
        ],
        "hints": [
            "Use a sliding window `[left, right]`.",
            "Keep track of characters seen and their most recent indices."
        ],
        "approach": "Sliding window with hash map storing last seen index of each character.",
        "starter_code": "def length_of_longest_substring(s):\n    # Write your solution here\n    # Return integer length\n    pass\n",
        "solution": "def length_of_longest_substring(s):\n    char_map = {}\n    left = 0\n    max_len = 0\n    for right, char in enumerate(s):\n        if char in char_map and char_map[char] >= left:\n            left = char_map[char] + 1\n        char_map[char] = right\n        max_len = max(max_len, right - left + 1)\n    return max_len\n",
        "test_cases": [
            {"args": ["abcabcbb"], "expected": 3},
            {"args": ["bbbbb"], "expected": 1},
            {"args": ["pwwkew"], "expected": 3}
        ]
    },
    {
        "id": "str_03",
        "title": "Minimum Window Substring",
        "topic": "Strings",
        "difficulty": "Hard",
        "statement": "Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return an empty string `\"\"`.",
        "examples": [
            {"input": "s = 'ADOBECODEBANC', t = 'ABC'", "output": "'BANC'", "explanation": "The minimum substring containing A, B, and C is 'BANC'."},
            {"input": "s = 'a', t = 'a'", "output": "'a'", "explanation": "Entire string is the minimum window."}
        ],
        "hints": [
            "Expand `right` until the window satisfies all character counts of `t`.",
            "Once valid, contract `left` to minimize length while retaining validity."
        ],
        "approach": "Two pointer sliding window with frequency counters and a count of matched unique characters.",
        "starter_code": "def min_window(s, t):\n    # Write your solution here\n    # Return string\n    pass\n",
        "solution": "from collections import Counter\ndef min_window(s, t):\n    if not s or not t:\n        return \"\"\n    target_counts = Counter(t)\n    window_counts = {}\n    have, need = 0, len(target_counts)\n    res, res_len = [-1, -1], float(\"inf\")\n    left = 0\n    for right, char in enumerate(s):\n        window_counts[char] = window_counts.get(char, 0) + 1\n        if char in target_counts and window_counts[char] == target_counts[char]:\n            have += 1\n        while have == need:\n            if (right - left + 1) < res_len:\n                res = [left, right]\n                res_len = right - left + 1\n            left_char = s[left]\n            window_counts[left_char] -= 1\n            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:\n                have -= 1\n            left += 1\n    return \"\" if res_len == float(\"inf\") else s[res[0]:res[1] + 1]\n",
        "test_cases": [
            {"args": ["ADOBECODEBANC", "ABC"], "expected": "BANC"},
            {"args": ["a", "a"], "expected": "a"},
            {"args": ["a", "aa"], "expected": ""}
        ]
    },

    # --- LINKED LISTS ---
    {
        "id": "ll_01",
        "title": "Reverse Linked List",
        "topic": "Linked Lists",
        "difficulty": "Easy",
        "statement": "Given the head of a singly linked list represented as a Python list of values, return the reversed list of values.",
        "examples": [
            {"input": "head = [1, 2, 3, 4, 5]", "output": "[5, 4, 3, 2, 1]", "explanation": "List is reversed."},
            {"input": "head = [1, 2]", "output": "[2, 1]", "explanation": "Two elements reversed."}
        ],
        "hints": [
            "In linked list node manipulation, maintain `prev`, `curr`, and `next` pointers.",
            "For arrays representing linked lists, reversing can be done in-place or iteratively."
        ],
        "approach": "Iterate while re-pointing `curr.next = prev`, or for list representation reverse in place.",
        "starter_code": "def reverse_list(head):\n    # Write your solution here\n    # head is a list of node values\n    pass\n",
        "solution": "def reverse_list(head):\n    return head[::-1]\n",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5]], "expected": [5, 4, 3, 2, 1]},
            {"args": [[1, 2]], "expected": [2, 1]},
            {"args": [[]], "expected": []}
        ]
    },
    {
        "id": "ll_02",
        "title": "Detect Cycle in Linked List",
        "topic": "Linked Lists",
        "difficulty": "Medium",
        "statement": "Given a list representing node connections where `edges[i]` is the next node index from node `i` (or -1 if end), return `True` if there is a cycle, else `False`.",
        "examples": [
            {"input": "edges = [1, 2, 3, 1]", "output": "True", "explanation": "Node 3 points back to node 1 forming a loop."},
            {"input": "edges = [1, 2, -1]", "output": "False", "explanation": "Node 2 points to -1 (end)."}
        ],
        "hints": [
            "Floyd's Cycle-Finding Algorithm (Tortoise and Hare) uses a slow and fast pointer.",
            "Alternatively, keep a set of visited node indices."
        ],
        "approach": "Fast and slow pointers move through indices. If fast catches slow, a cycle exists.",
        "starter_code": "def has_cycle(edges):\n    # edges[i] is next node index from i, or -1\n    pass\n",
        "solution": "def has_cycle(edges):\n    if not edges:\n        return False\n    visited = set()\n    curr = 0\n    while curr != -1 and curr < len(edges):\n        if curr in visited:\n            return True\n        visited.add(curr)\n        curr = edges[curr]\n    return False\n",
        "test_cases": [
            {"args": [[1, 2, 3, 1]], "expected": True},
            {"args": [[1, 2, -1]], "expected": False},
            {"args": [[-1]], "expected": False}
        ]
    },

    # --- STACKS ---
    {
        "id": "stk_01",
        "title": "Valid Parentheses",
        "topic": "Stacks",
        "difficulty": "Easy",
        "statement": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.",
        "examples": [
            {"input": "s = '()[]{}'", "output": "True", "explanation": "Every bracket is closed in the right order."},
            {"input": "s = '(]'", "output": "False", "explanation": "Mismatched brackets."}
        ],
        "hints": [
            "Use a stack to push opening brackets.",
            "When encountering a closing bracket, check if it matches the top of the stack."
        ],
        "approach": "Stack of characters with a dictionary of closing-to-opening bracket pairs.",
        "starter_code": "def is_valid_parentheses(s):\n    # Write your solution here\n    # Return boolean\n    pass\n",
        "solution": "def is_valid_parentheses(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top_element = stack.pop() if stack else '#'\n            if mapping[char] != top_element:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
        "test_cases": [
            {"args": ["()[]{}"], "expected": True},
            {"args": ["(]"], "expected": False},
            {"args": ["([{}])"], "expected": True}
        ]
    },
    {
        "id": "stk_02",
        "title": "Daily Temperatures",
        "topic": "Stacks",
        "difficulty": "Medium",
        "statement": "Given an array of integers `temperatures` represents daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature. If no warmer day exists, keep `answer[i] == 0`.",
        "examples": [
            {"input": "temperatures = [73, 74, 75, 71, 69, 72, 76, 73]", "output": "[1, 1, 4, 2, 1, 1, 0, 0]", "explanation": "73 is followed immediately by 74 (1 day wait), etc."}
        ],
        "hints": [
            "Maintain a monotonic decreasing stack storing indices.",
            "When current temp > temp at stack top index, pop and calculate difference in indices."
        ],
        "approach": "Monotonic Stack storing indices of temperatures that haven't found a warmer day yet.",
        "starter_code": "def daily_temperatures(temperatures):\n    # Write your solution here\n    pass\n",
        "solution": "def daily_temperatures(temperatures):\n    n = len(temperatures)\n    ans = [0] * n\n    stack = []\n    for i, t in enumerate(temperatures):\n        while stack and temperatures[stack[-1]] < t:\n            prev_index = stack.pop()\n            ans[prev_index] = i - prev_index\n        stack.append(i)\n    return ans\n",
        "test_cases": [
            {"args": [[73, 74, 75, 71, 69, 72, 76, 73]], "expected": [1, 1, 4, 2, 1, 1, 0, 0]},
            {"args": [[30, 40, 50, 60]], "expected": [1, 1, 1, 0]}
        ]
    },

    # --- QUEUES ---
    {
        "id": "que_01",
        "title": "Implement Queue using Stacks",
        "topic": "Queues",
        "difficulty": "Easy",
        "statement": "Implement a first-in first-out (FIFO) queue simulation using two stacks. Function `simulate_queue(operations, values)` takes lists of commands (`'push'`, `'pop'`, `'peek'`) and returns results of pop/peek operations.",
        "examples": [
            {"input": "operations = ['push', 'push', 'peek', 'pop'], values = [1, 2, None, None]", "output": "[1, 1]", "explanation": "peek returned 1, pop returned 1."}
        ],
        "hints": [
            "Use an `in_stack` for enqueue and `out_stack` for dequeue.",
            "Transfer from `in_stack` to `out_stack` only when `out_stack` is empty."
        ],
        "approach": "Two-stack amortized O(1) queue algorithm.",
        "starter_code": "def simulate_queue(operations, values):\n    # Return list of results for 'pop' and 'peek'\n    pass\n",
        "solution": "def simulate_queue(operations, values):\n    in_stack = []\n    out_stack = []\n    res = []\n    for op, val in zip(operations, values):\n        if op == 'push':\n            in_stack.append(val)\n        elif op in ('pop', 'peek'):\n            if not out_stack:\n                while in_stack:\n                    out_stack.append(in_stack.pop())\n            if out_stack:\n                item = out_stack.pop() if op == 'pop' else out_stack[-1]\n                res.append(item)\n    return res\n",
        "test_cases": [
            {"args": [["push", "push", "peek", "pop"], [1, 2, None, None]], "expected": [1, 1]}
        ]
    },

    # --- HASHING ---
    {
        "id": "hash_01",
        "title": "Group Anagrams",
        "topic": "Hashing",
        "difficulty": "Medium",
        "statement": "Given an array of strings `strs`, group the anagrams together. Return the grouped lists (sorted lexicographically by group).",
        "examples": [
            {"input": "strs = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']", "output": "[['bat'], ['nat', 'tan'], ['ate', 'eat', 'tea']]", "explanation": "Anagrams are clustered."}
        ],
        "hints": [
            "Two strings are anagrams if their sorted characters are identical.",
            "Use the sorted string as a dictionary key."
        ],
        "approach": "Hash map with key as sorted character tuple, values as list of original strings.",
        "starter_code": "def group_anagrams(strs):\n    # Write your solution here\n    pass\n",
        "solution": "from collections import defaultdict\ndef group_anagrams(strs):\n    groups = defaultdict(list)\n    for s in strs:\n        key = tuple(sorted(s))\n        groups[key].append(s)\n    res = [sorted(g) for g in groups.values()]\n    return sorted(res, key=lambda x: (len(x), x))\n",
        "test_cases": [
            {"args": [["eat", "tea", "tan", "ate", "nat", "bat"]], "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]}
        ]
    },

    # --- RECURSION ---
    {
        "id": "rec_01",
        "title": "Subsets (Power Set)",
        "topic": "Recursion",
        "difficulty": "Medium",
        "statement": "Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return subsets sorted.",
        "examples": [
            {"input": "nums = [1, 2, 3]", "output": "[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]", "explanation": "All 2^3 = 8 subsets."}
        ],
        "hints": [
            "At each index, you either include `nums[i]` or exclude it in the subset.",
            "Use backtracking or cascading generation."
        ],
        "approach": "Backtracking recursion: `backtrack(start, current_subset)`.",
        "starter_code": "def subsets(nums):\n    # Return list of sorted subsets\n    pass\n",
        "solution": "def subsets(nums):\n    res = []\n    def backtrack(start, curr):\n        res.append(list(curr))\n        for i in range(start, len(nums)):\n            curr.append(nums[i])\n            backtrack(i + 1, curr)\n            curr.pop()\n    backtrack(0, [])\n    return sorted(res, key=lambda x: (len(x), x))\n",
        "test_cases": [
            {"args": [[1, 2]], "expected": [[], [1], [2], [1, 2]]}
        ]
    },

    # --- SORTING ---
    {
        "id": "sort_01",
        "title": "Merge Intervals",
        "topic": "Sorting",
        "difficulty": "Medium",
        "statement": "Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all intervals in input.",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Intervals [1,3] and [2,6] overlap, merged into [1,6]."}
        ],
        "hints": [
            "First sort intervals by starting coordinate.",
            "Compare current start with the previous interval's end."
        ],
        "approach": "Sort by interval start time, then sequentially merge overlapping intervals.",
        "starter_code": "def merge_intervals(intervals):\n    # Write your solution here\n    pass\n",
        "solution": "def merge_intervals(intervals):\n    if not intervals:\n        return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for current in intervals[1:]:\n        prev = merged[-1]\n        if current[0] <= prev[1]:\n            prev[1] = max(prev[1], current[1])\n        else:\n            merged.append(current)\n    return merged\n",
        "test_cases": [
            {"args": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]},
            {"args": [[[1, 4], [4, 5]]], "expected": [[1, 5]]}
        ]
    },

    # --- SEARCHING ---
    {
        "id": "srch_01",
        "title": "Binary Search",
        "topic": "Searching",
        "difficulty": "Easy",
        "statement": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, return its index. Otherwise, return -1.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 exists in nums and its index is 4."}
        ],
        "hints": [
            "Divide and conquer by maintaining `low` and `high` pointers.",
            "Compute `mid = (low + high) // 2`."
        ],
        "approach": "Classical binary search in O(log n) time.",
        "starter_code": "def search(nums, target):\n    # Write your solution here\n    pass\n",
        "solution": "def search(nums, target):\n    low, high = 0, len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n",
        "test_cases": [
            {"args": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4},
            {"args": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1}
        ]
    },

    # --- TREES ---
    {
        "id": "tree_01",
        "title": "Maximum Depth of Binary Tree",
        "topic": "Trees",
        "difficulty": "Easy",
        "statement": "Given a binary tree represented as a nested dictionary `{'val': int, 'left': node, 'right': node}` or `None`, find its maximum depth. Maximum depth is the number of nodes along the longest path from root to leaf.",
        "examples": [
            {"input": "root = {'val': 3, 'left': {'val': 9, 'left': None, 'right': None}, 'right': {'val': 20, 'left': None, 'right': None}}", "output": "2", "explanation": "Depth is 2."}
        ],
        "hints": [
            "If node is None, depth is 0.",
            "Recursively calculate `1 + max(depth(left), depth(right))`."
        ],
        "approach": "Recursive depth-first traversal.",
        "starter_code": "def max_depth(root):\n    # root is dict {'val', 'left', 'right'} or None\n    pass\n",
        "solution": "def max_depth(root):\n    if not root:\n        return 0\n    return 1 + max(max_depth(root.get('left')), max_depth(root.get('right')))\n",
        "test_cases": [
            {"args": [{"val": 3, "left": {"val": 9, "left": None, "right": None}, "right": {"val": 20, "left": None, "right": None}}], "expected": 2},
            {"args": [None], "expected": 0}
        ]
    },

    # --- BINARY SEARCH TREES ---
    {
        "id": "bst_01",
        "title": "Validate Binary Search Tree",
        "topic": "Binary Search Trees",
        "difficulty": "Medium",
        "statement": "Given the root of a binary tree represented as nested dictionary `{'val': int, 'left': node, 'right': node}` or `None`, determine if it is a valid binary search tree (BST).",
        "examples": [
            {"input": "root = {'val': 2, 'left': {'val': 1, 'left': None, 'right': None}, 'right': {'val': 3, 'left': None, 'right': None}}", "output": "True", "explanation": "Valid BST."}
        ],
        "hints": [
            "Every left subtree node must be strictly less than the node's value.",
            "Every right subtree node must be strictly greater than the node's value."
        ],
        "approach": "Validate using lower and upper bounds `(low, high)` updated recursively.",
        "starter_code": "def is_valid_bst(root):\n    # Write your solution here\n    pass\n",
        "solution": "def is_valid_bst(root):\n    def validate(node, low=float('-inf'), high=float('inf')):\n        if not node:\n            return True\n        val = node['val']\n        if val <= low or val >= high:\n            return False\n        return validate(node.get('left'), low, val) and validate(node.get('right'), val, high)\n    return validate(root)\n",
        "test_cases": [
            {"args": [{"val": 2, "left": {"val": 1, "left": None, "right": None}, "right": {"val": 3, "left": None, "right": None}}], "expected": True},
            {"args": [{"val": 5, "left": {"val": 1, "left": None, "right": None}, "right": {"val": 4, "left": None, "right": None}}], "expected": False}
        ]
    },

    # --- HEAPS ---
    {
        "id": "heap_01",
        "title": "Kth Largest Element in an Array",
        "topic": "Heaps",
        "difficulty": "Medium",
        "statement": "Given an integer array `nums` and an integer `k`, return the `k-th` largest element in the array. Note that it is the `k-th` largest element in the sorted order, not the `k-th` distinct element.",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5", "explanation": "2nd largest element is 5."},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4", "explanation": "4th largest element is 4."}
        ],
        "hints": [
            "You can maintain a min-heap of size `k`.",
            "When the heap exceeds size `k`, pop the minimum element."
        ],
        "approach": "Min-heap of size k storing top k elements. The top of the heap is the k-th largest element.",
        "starter_code": "def find_kth_largest(nums, k):\n    # Write your solution here\n    pass\n",
        "solution": "import heapq\ndef find_kth_largest(nums, k):\n    min_heap = []\n    for num in nums:\n        heapq.heappush(min_heap, num)\n        if len(min_heap) > k:\n            heapq.heappop(min_heap)\n    return min_heap[0]\n",
        "test_cases": [
            {"args": [[3, 2, 1, 5, 6, 4], 2], "expected": 5},
            {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expected": 4}
        ]
    },

    # --- GRAPHS ---
    {
        "id": "graph_01",
        "title": "Number of Connected Components in an Undirected Graph",
        "topic": "Graphs",
        "difficulty": "Medium",
        "statement": "You have a graph of `n` nodes labeled `0` to `n - 1`. You are given an integer `n` and an array `edges` where `edges[i] = [a, b]` indicates an undirected edge between `a` and `b`. Return the total number of connected components.",
        "examples": [
            {"input": "n = 5, edges = [[0,1],[1,2],[3,4]]", "output": "2", "explanation": "Component 1: {0,1,2}, Component 2: {3,4}."}
        ],
        "hints": [
            "Build an adjacency list representation of the graph.",
            "Perform BFS or DFS from each unvisited node to count components."
        ],
        "approach": "Depth-First Search (DFS) or Disjoint Set Union (DSU) to count components.",
        "starter_code": "def count_components(n, edges):\n    # Write your solution here\n    pass\n",
        "solution": "from collections import defaultdict\ndef count_components(n, edges):\n    graph = defaultdict(list)\n    for u, v in edges:\n        graph[u].append(v)\n        graph[v].append(u)\n    visited = set()\n    components = 0\n    for i in range(n):\n        if i not in visited:\n            components += 1\n            stack = [i]\n            visited.add(i)\n            while stack:\n                node = stack.pop()\n                for neighbor in graph[node]:\n                    if neighbor not in visited:\n                        visited.add(neighbor)\n                        stack.append(neighbor)\n    return components\n",
        "test_cases": [
            {"args": [5, [[0, 1], [1, 2], [3, 4]]], "expected": 2},
            {"args": [5, [[0, 1], [1, 2], [2, 3], [3, 4]]], "expected": 1}
        ]
    },

    # --- DYNAMIC PROGRAMMING ---
    {
        "id": "dp_01",
        "title": "Climbing Stairs",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "statement": "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "1 step + 1 step, or 2 steps."},
            {"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, 2+1."}
        ],
        "hints": [
            "To reach step n, you must arrive from step n-1 or step n-2.",
            "ways(n) = ways(n-1) + ways(n-2), similar to Fibonacci."
        ],
        "approach": "Bottom-up dynamic programming storing previous two values.",
        "starter_code": "def climb_stairs(n):\n    # Write your solution here\n    pass\n",
        "solution": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n",
        "test_cases": [
            {"args": [2], "expected": 2},
            {"args": [3], "expected": 3},
            {"args": [5], "expected": 8}
        ]
    },
    {
        "id": "dp_02",
        "title": "Coin Change",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "statement": "Given an integer array `coins` representing coins of different denominations and an integer `amount`, return the fewest number of coins that you need to make up that amount. If impossible, return -1.",
        "examples": [
            {"input": "coins = [1, 2, 5], amount = 11", "output": "3", "explanation": "11 = 5 + 5 + 1."},
            {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Cannot make amount 3 with coin of 2."}
        ],
        "hints": [
            "Define `dp[i]` as the minimum coins needed for amount `i`.",
            "For each coin `c`, `dp[i] = min(dp[i], dp[i - c] + 1)`."
        ],
        "approach": "1D Bottom-up DP array initialized to infinity.",
        "starter_code": "def coin_change(coins, amount):\n    # Write your solution here\n    pass\n",
        "solution": "def coin_change(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for i in range(1, amount + 1):\n        for coin in coins:\n            if i - coin >= 0:\n                dp[i] = min(dp[i], dp[i - coin] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1\n",
        "test_cases": [
            {"args": [[1, 2, 5], 11], "expected": 3},
            {"args": [[2], 3], "expected": -1},
            {"args": [[1], 0], "expected": 0}
        ]
    }
]

def get_all_dsa_questions():
    """Return all DSA questions."""
    return DSA_QUESTIONS

def get_dsa_question_by_id(qid):
    """Retrieve single question by id."""
    for q in DSA_QUESTIONS:
        if q["id"] == qid:
            return q
    return None

def filter_dsa_questions(topic=None, difficulty=None, search_term=None):
    """Filter DSA questions based on criteria."""
    filtered = DSA_QUESTIONS
    if topic and topic != "All":
        filtered = [q for q in filtered if q["topic"] == topic]
    if difficulty and difficulty != "All":
        filtered = [q for q in filtered if q["difficulty"] == difficulty]
    if search_term:
        term = search_term.lower()
        filtered = [q for q in filtered if term in q["title"].lower() or term in q["statement"].lower()]
    return filtered
