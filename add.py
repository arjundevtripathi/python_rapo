# import streamlit as st 
# st.set_page_config(page_title="Number Addition",page_icon="➕",layout="centered")
# st.title("Addition of Two Number")
# st.caption("Enter you Two number and it return addition of them")

# form = st.form("add_form")
# num1 = form.number_input("First Number")
# num2 = form.number_input("Second Number")
# submitted=form.form_submit_button("Calculate Sum")

# if submitted:
#     result=num1+num2
#     st.divider()
#     st.metric(label="Result",value="result")

"""
╔══════════════════════════════════════════════════════════════════════╗
║   Python LIST – Complete Streamlit Reference App                     ║
║   All Methods · All Built-in Functions · 100 Code Examples           ║
║   Run:  streamlit run streamlit_list_reference.py                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import random
import time
import math
import copy
import bisect
import heapq
from collections import Counter, defaultdict, deque, OrderedDict
from itertools import (
    accumulate, chain, combinations, permutations, product as iproduct
)
from functools import reduce

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Python List – Complete Reference",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── global ── */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
.main .block-container { padding-top: 1rem; padding-bottom: 2rem; }

/* ── hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero h1 { color: #e94560; font-size: 2.6rem; margin: 0; }
.hero p  { color: #a8dadc; font-size: 1.1rem; margin-top: 0.5rem; }

/* ── section header ── */
.sec-header {
    background: linear-gradient(90deg, #e94560, #0f3460);
    color: white;
    padding: 0.55rem 1.2rem;
    border-radius: 8px;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 1.2rem 0 0.8rem 0;
}

/* ── method / example card ── */
.card {
    background: #1e1e2e;
    border: 1px solid #2d2d3f;
    border-left: 4px solid #e94560;
    border-radius: 10px;
    padding: 1rem 1.2rem 0.7rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.card-title {
    color: #e94560;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.card-def {
    color: #a8dadc;
    font-size: 0.88rem;
    margin-bottom: 0.6rem;
    font-style: italic;
}
.card-syntax {
    background: #12121f;
    color: #c9d1d9;
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    font-family: 'Courier New', monospace;
    font-size: 0.83rem;
    border-left: 3px solid #58a6ff;
    white-space: pre-wrap;
}

/* ── example number badge ── */
.badge-beg  { background:#2e7d32; color:white; padding:2px 8px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-int  { background:#1565c0; color:white; padding:2px 8px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-adv  { background:#6a1b9a; color:white; padding:2px 8px; border-radius:12px; font-size:0.78rem; font-weight:700; }

/* ── stat boxes ── */
.stat-row { display:flex; gap:1rem; margin-bottom:1.2rem; flex-wrap:wrap; }
.stat-box {
    flex:1; min-width:120px;
    background:#1e1e2e;
    border:1px solid #2d2d3f;
    border-radius:10px;
    padding:0.8rem 1rem;
    text-align:center;
}
.stat-num { font-size:1.8rem; font-weight:800; color:#e94560; }
.stat-lbl { color:#8b949e; font-size:0.78rem; }

/* ── interactive output box ── */
.out-box {
    background:#0d1117;
    color:#58a6ff;
    border-radius:8px;
    padding:0.7rem 1rem;
    font-family:'Courier New', monospace;
    font-size:0.85rem;
    margin-top:0.5rem;
    border:1px solid #21262d;
    white-space: pre-wrap;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] { background:#0d1117 !important; }
section[data-testid="stSidebar"] * { color:#c9d1d9 !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# DATA DEFINITIONS
# ──────────────────────────────────────────────────────────────

LIST_METHODS = [
    {
        "name": "append(x)",
        "syntax": "list.append(x)",
        "definition": "Add a single item x to the END of the list. Mutates in place. Returns None.",
        "example": '>>> fruits = ["apple", "banana"]\n>>> fruits.append("cherry")\n>>> fruits\n[\'apple\', \'banana\', \'cherry\']',
        "time": "O(1) amortized",
        "tip": "append() vs extend(): append adds ONE item; extend adds ALL items from an iterable.",
    },
    {
        "name": "extend(iterable)",
        "syntax": "list.extend(iterable)",
        "definition": "Append all items from an iterable (list, tuple, string, generator…) to the end of the list.",
        "example": '>>> a = [1, 2]\n>>> a.extend([3, 4])\n>>> a\n[1, 2, 3, 4]',
        "time": "O(k) where k = len(iterable)",
        "tip": "Equivalent to: a += [3, 4]",
    },
    {
        "name": "insert(i, x)",
        "syntax": "list.insert(i, x)",
        "definition": "Insert item x BEFORE index i. All elements at i and beyond shift right by one.",
        "example": '>>> nums = [1, 2, 4, 5]\n>>> nums.insert(2, 3)\n>>> nums\n[1, 2, 3, 4, 5]',
        "time": "O(n) — shifts elements",
        "tip": "insert(0, x) prepends. insert(len(lst), x) is same as append(x).",
    },
    {
        "name": "remove(x)",
        "syntax": "list.remove(x)",
        "definition": "Remove the FIRST occurrence of value x. Raises ValueError if x is not in the list.",
        "example": '>>> a = [1, 2, 3, 2]\n>>> a.remove(2)\n>>> a\n[1, 3, 2]',
        "time": "O(n) — searches linearly",
        "tip": "Only removes FIRST match. Use list comprehension to remove ALL occurrences.",
    },
    {
        "name": "pop([i])",
        "syntax": "list.pop([i])",
        "definition": "Remove and RETURN item at index i (default: last). Raises IndexError if list is empty.",
        "example": '>>> stack = [10, 20, 30]\n>>> stack.pop()   # 30\n>>> stack.pop(0)  # 10\n>>> stack\n[20]',
        "time": "O(1) from end; O(n) from middle",
        "tip": "pop() from end is O(1) — use list as a stack. pop(0) is O(n) — use deque for queue.",
    },
    {
        "name": "clear()",
        "syntax": "list.clear()",
        "definition": "Remove ALL items from the list. Equivalent to del lst[:]. The list object itself remains.",
        "example": '>>> data = [1, 2, 3]\n>>> data.clear()\n>>> data\n[]',
        "time": "O(n)",
        "tip": "clear() keeps the same list object (id unchanged). del lst would destroy the reference.",
    },
    {
        "name": "index(x[, start[, end]])",
        "syntax": "list.index(x, start=0, end=len(list))",
        "definition": "Return the index of the FIRST occurrence of x in slice [start:end]. Raises ValueError if not found.",
        "example": '>>> a = ["a","b","c","b"]\n>>> a.index("b")      # 1\n>>> a.index("b", 2)   # 3',
        "time": "O(n)",
        "tip": "Use 'x in lst' to check existence before calling index() to avoid ValueError.",
    },
    {
        "name": "count(x)",
        "syntax": "list.count(x)",
        "definition": "Return the number of times value x appears in the list.",
        "example": '>>> a = [1, 2, 1, 3, 1]\n>>> a.count(1)   # 3\n>>> a.count(4)   # 0',
        "time": "O(n)",
        "tip": "For large lists, Counter(lst) is more efficient when counting multiple values.",
    },
    {
        "name": "sort(key=None, reverse=False)",
        "syntax": "list.sort(*, key=None, reverse=False)",
        "definition": "Sort the list IN PLACE using Timsort. key= is a one-arg function; reverse=True for descending.",
        "example": '>>> a = [3,1,4,1,5]\n>>> a.sort()\n>>> a\n[1, 1, 3, 4, 5]',
        "time": "O(n log n)",
        "tip": "sort() mutates in place and returns None. Use sorted() to get a NEW sorted list.",
    },
    {
        "name": "reverse()",
        "syntax": "list.reverse()",
        "definition": "Reverse the list IN PLACE. Returns None. Uses O(1) extra space.",
        "example": '>>> a = [1, 2, 3]\n>>> a.reverse()\n>>> a\n[3, 2, 1]',
        "time": "O(n)",
        "tip": "reversed(lst) returns an iterator without mutating. lst[::-1] creates a reversed copy.",
    },
    {
        "name": "copy()",
        "syntax": "list.copy()",
        "definition": "Return a SHALLOW copy of the list. Nested objects are still shared between original and copy.",
        "example": '>>> a = [1, [2, 3]]\n>>> b = a.copy()\n>>> b[0] = 99        # does NOT affect a\n>>> b[1][0] = 99     # DOES affect a (shared inner list)',
        "time": "O(n)",
        "tip": "For full independence of nested objects, use copy.deepcopy(lst).",
    },
]

BUILTIN_FUNCTIONS = [
    {"name": "len(lst)", "definition": "Return the number of items in the list.", "example": "len([1,2,3]) → 3"},
    {"name": "max(lst)", "definition": "Return the largest item. Accepts key= argument.", "example": "max([3,1,4]) → 4"},
    {"name": "min(lst)", "definition": "Return the smallest item. Accepts key= argument.", "example": "min([3,1,4]) → 1"},
    {"name": "sum(lst, start=0)", "definition": "Return sum of all numeric items plus start.", "example": "sum([1,2,3]) → 6"},
    {"name": "sorted(lst)", "definition": "Return a NEW sorted list without mutating original.", "example": "sorted([3,1,2]) → [1,2,3]"},
    {"name": "reversed(lst)", "definition": "Return a reverse iterator (not a list).", "example": "list(reversed([1,2,3])) → [3,2,1]"},
    {"name": "enumerate(lst)", "definition": "Return (index, value) pairs. start= parameter sets first index.", "example": "list(enumerate(['a','b'])) → [(0,'a'),(1,'b')]"},
    {"name": "zip(*lists)", "definition": "Combine iterables element-by-element into tuples.", "example": "list(zip([1,2],[3,4])) → [(1,3),(2,4)]"},
    {"name": "map(fn, lst)", "definition": "Apply fn to every element; returns an iterator.", "example": "list(map(str,[1,2,3])) → ['1','2','3']"},
    {"name": "filter(fn, lst)", "definition": "Keep elements where fn(x) is True; returns iterator.", "example": "list(filter(bool,[0,1,'',2])) → [1,2]"},
    {"name": "any(lst)", "definition": "Return True if at least one element is truthy.", "example": "any([0,0,1]) → True"},
    {"name": "all(lst)", "definition": "Return True if ALL elements are truthy.", "example": "all([1,2,3]) → True"},
    {"name": "list(iterable)", "definition": "Convert any iterable to a list.", "example": "list('abc') → ['a','b','c']"},
    {"name": "id(lst)", "definition": "Return unique identity (memory address) of the list object.", "example": "id([]) → some integer"},
    {"name": "isinstance(x, list)", "definition": "Check if object is a list instance.", "example": "isinstance([1,2], list) → True"},
    {"name": "del lst[i]", "definition": "Delete element at index i or a slice.", "example": "del lst[0] removes first item"},
    {"name": "in / not in", "definition": "Membership test; returns bool.", "example": "3 in [1,2,3] → True"},
]

# 100 examples data: (num, title, level, definition, code)
EXAMPLES = [
    # ── BEGINNER 1-30 ──
    (1, "Create a list", "Beginner",
     "Use [] to create a list with any mix of data types. Lists are ordered and mutable.",
     """fruits = ['apple', 'banana', 'cherry']
nums   = [1, 2, 3, 4, 5]
mixed  = [42, 'hello', 3.14, True, None]
empty  = []
print(fruits)
print(nums)
print(mixed)"""),

    (2, "Access elements by index", "Beginner",
     "Lists are zero-indexed. Positive indices count from the start; negative from the end.",
     """lst = ['a', 'b', 'c', 'd', 'e']
print(lst[0])    # 'a'  ← first
print(lst[2])    # 'c'
print(lst[-1])   # 'e'  ← last
print(lst[-2])   # 'd'"""),

    (3, "Modify an element", "Beginner",
     "Lists are mutable — assign a new value to any index to update it.",
     """colors = ['red', 'green', 'blue']
colors[1] = 'yellow'
print(colors)   # ['red', 'yellow', 'blue']
colors[-1] = 'purple'
print(colors)   # ['red', 'yellow', 'purple']"""),

    (4, "len() — list length", "Beginner",
     "len() returns the total number of top-level items in the list.",
     """data = [10, 20, 30, 40, 50]
print(len(data))     # 5
print(len([]))       # 0
print(len([[1,2]]))  # 1 (nested list counts as ONE item)"""),

    (5, "append() and extend()", "Beginner",
     "append() adds ONE item; extend() unpacks and adds ALL items from an iterable.",
     """lst = [1, 2, 3]
lst.append(4)
print(lst)       # [1, 2, 3, 4]
lst.extend([5, 6, 7])
print(lst)       # [1, 2, 3, 4, 5, 6, 7]

# KEY DIFFERENCE:
a = [1, 2]; a.append([3, 4])  # nested → [1,2,[3,4]]
b = [1, 2]; b.extend([3, 4])  # flat   → [1,2,3,4]
print(a, b)"""),

    (6, "Basic slicing [start:stop]", "Beginner",
     "Slicing returns a NEW list from index start (inclusive) to stop (exclusive).",
     """nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])   # [2, 3, 4]
print(nums[:4])    # [0, 1, 2, 3]
print(nums[6:])    # [6, 7, 8, 9]
print(nums[:])     # full copy"""),

    (7, "Slicing with step [::step]", "Beginner",
     "The third slice parameter controls the step. Negative step reverses the list.",
     """nums = list(range(10))
print(nums[::2])    # [0,2,4,6,8] every 2nd
print(nums[1::2])   # [1,3,5,7,9] odd indices
print(nums[::-1])   # [9,8,...,0] reversed"""),

    (8, "Membership: in / not in", "Beginner",
     "'in' returns True if the value exists anywhere in the list. O(n) scan.",
     """fruits = ['apple', 'banana', 'cherry']
print('apple'  in fruits)      # True
print('mango'  in fruits)      # False
print('mango'  not in fruits)  # True"""),

    (9, "for loop over a list", "Beginner",
     "A for loop visits each element. Use enumerate() to also get the index.",
     """colors = ['red', 'green', 'blue']
for color in colors:
    print(color.upper())

for i, color in enumerate(colors, start=1):
    print(f'{i}. {color}')"""),

    (10, "Concatenation with +", "Beginner",
     "The + operator joins two lists into a new list. Neither original is modified.",
     """a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
print(c)   # [1, 2, 3, 4, 5, 6]
print(a)   # [1, 2, 3] ← unchanged"""),

    (11, "Repetition with *", "Beginner",
     "Multiply a list by n to repeat its elements n times.",
     """zeros   = [0] * 5
print(zeros)    # [0,0,0,0,0]
pattern = [1, 2] * 3
print(pattern)  # [1,2,1,2,1,2]"""),

    (12, "insert() and remove()", "Beginner",
     "insert(i,x) places x before index i; remove(x) deletes the first match of x.",
     """lst = [1, 2, 4, 5]
lst.insert(2, 3)
print(lst)   # [1, 2, 3, 4, 5]
lst.remove(3)
print(lst)   # [1, 2, 4, 5]"""),

    (13, "pop() — remove & return", "Beginner",
     "pop() removes and returns the last item (or item at given index).",
     """stack = ['a', 'b', 'c', 'd']
print(stack.pop())     # 'd'
print(stack)           # ['a','b','c']
print(stack.pop(0))    # 'a'
print(stack)           # ['b','c']"""),

    (14, "sort() and sorted()", "Beginner",
     "sort() sorts in place (returns None). sorted() returns a new sorted list.",
     """nums = [3, 1, 4, 1, 5, 9]
nums.sort()
print(nums)                    # [1,1,3,4,5,9]
nums.sort(reverse=True)
print(nums)                    # [9,5,4,3,1,1]
words = ['banana','apple','fig']
print(sorted(words))           # ['apple','banana','fig']"""),

    (15, "count() and index()", "Beginner",
     "count(x) counts occurrences; index(x) finds the position of the first match.",
     """lst = [1, 2, 3, 2, 1, 2]
print(lst.count(2))    # 3
print(lst.index(2))    # 1 (first occurrence)
print(lst.index(2, 2)) # 3 (search from index 2)"""),

    (16, "reverse() and [::-1]", "Beginner",
     "reverse() reverses in place. Slicing [::-1] returns a reversed copy.",
     """lst = [1, 2, 3, 4, 5]
lst.reverse()
print(lst)           # [5,4,3,2,1]

original = [1, 2, 3, 4, 5]
rev_copy = original[::-1]
print(original)      # [1,2,3,4,5] ← unchanged
print(rev_copy)      # [5,4,3,2,1]"""),

    (17, "list(range(...))", "Beginner",
     "list(range(n)) creates a list of consecutive integers.",
     """print(list(range(10)))           # [0..9]
print(list(range(1, 11)))        # [1..10]
print(list(range(0, 20, 2)))     # evens
print(list(range(10, 0, -1)))    # countdown"""),

    (18, "Nested lists (2D matrix)", "Beginner",
     "A list can hold other lists, forming a 2D grid. Access with [row][col].",
     """matrix = [[1,2,3],[4,5,6],[7,8,9]]
print(matrix[1][2])  # 6
for row in matrix:
    print(row)"""),

    (19, "copy() — shallow copy", "Beginner",
     "copy() creates a new list with the same top-level elements (shared nested objects).",
     """original = [1, 2, [3, 4]]
shallow  = original.copy()
shallow[0] = 99          # safe — doesn't affect original
print(original[0])       # 1
shallow[2][0] = 999      # UNSAFE — shared inner list
print(original[2][0])    # 999"""),

    (20, "join() — list to string", "Beginner",
     "str.join(list) concatenates a list of strings with the separator.",
     """words = ['Python', 'is', 'awesome']
print(' '.join(words))    # Python is awesome
print('-'.join(words))    # Python-is-awesome
nums = [1,2,3,4,5]
print(','.join(str(n) for n in nums))  # 1,2,3,4,5"""),

    (21, "sum(), max(), min()", "Beginner",
     "Built-in functions for quick numeric analysis of a list.",
     """nums = [4, 2, 9, 7, 5, 1, 8, 3, 6]
print('Sum:', sum(nums))
print('Max:', max(nums))
print('Min:', min(nums))
print('Avg:', sum(nums) / len(nums))"""),

    (22, "del — delete elements", "Beginner",
     "del removes an element by index or deletes an entire slice.",
     """lst = [0, 1, 2, 3, 4, 5]
del lst[0]
print(lst)      # [1,2,3,4,5]
del lst[1:3]
print(lst)      # [1,4,5]"""),

    (23, "Unpacking a list", "Beginner",
     "Assign list items to variables. Use * to capture the rest.",
     """lst = [10, 20, 30, 40, 50]
a, b, c, d, e = lst
print(a, b, c)

first, *middle, last = lst
print(first, middle, last)  # 10 [20,30,40] 50"""),

    (24, "List as stack (LIFO)", "Beginner",
     "Use append() to push and pop() to pop — O(1) stack operations.",
     """stack = []
stack.append('page1')
stack.append('page2')
stack.append('page3')
print(stack.pop())   # page3 — LIFO
print(stack.pop())   # page2
print(stack)"""),

    (25, "List as queue (FIFO)", "Beginner",
     "Use collections.deque for O(1) FIFO. Plain list pop(0) is O(n).",
     """from collections import deque
queue = deque()
queue.append('task1')
queue.append('task2')
queue.append('task3')
print(queue.popleft())  # task1 — FIFO
print(queue.popleft())  # task2"""),

    (26, "any() and all()", "Beginner",
     "any() → True if ≥1 element is truthy. all() → True if every element is truthy.",
     """nums = [2, 4, 6, 7, 8]
print(any(x % 2 != 0 for x in nums))  # True (7 is odd)
print(all(x > 0 for x in nums))       # True
print(all(x % 2 == 0 for x in nums))  # False"""),

    (27, "Swap two elements", "Beginner",
     "Python's tuple unpacking swaps two values without a temp variable.",
     """lst = [1, 2, 3, 4, 5]
lst[0], lst[-1] = lst[-1], lst[0]
print(lst)   # [5,2,3,4,1]"""),

    (28, "Check if list is empty", "Beginner",
     "An empty list is falsy. Use 'not lst' or len() == 0.",
     """empty = []
data  = [1, 2]
print(bool(empty))   # False
print(bool(data))    # True
if not empty:
    print('empty list!')
if data:
    print('has items!')"""),

    (29, "Flatten a 2D list", "Beginner",
     "Nested list comprehension with two for clauses flattens one level.",
     """matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat = [x for row in matrix for x in row]
print(flat)   # [1,2,3,4,5,6,7,8,9]"""),

    (30, "Remove duplicates (preserve order)", "Beginner",
     "dict.fromkeys() preserves insertion order and removes duplicates.",
     """lst = [3,1,4,1,5,9,2,6,5,3,5]
unique = list(dict.fromkeys(lst))
print(unique)   # [3,1,4,5,9,2,6]"""),

    # ── INTERMEDIATE 31-70 ──
    (31, "Basic list comprehension", "Intermediate",
     "[expression for item in iterable] — concise list creation.",
     """squares = [x**2 for x in range(1, 11)]
print(squares)
cubes = [x**3 for x in range(1, 6)]
print(cubes)"""),

    (32, "Comprehension with filter", "Intermediate",
     "Add 'if condition' at the end to include only matching elements.",
     """evens = [x for x in range(20) if x % 2 == 0]
print(evens)
big_squares = [x**2 for x in range(20) if x**2 > 100]
print(big_squares)"""),

    (33, "Comprehension with if-else transform", "Intermediate",
     "Place 'value_if_true if condition else value_if_false' BEFORE the for.",
     """nums = range(1, 11)
labels = ['even' if x%2==0 else 'odd' for x in nums]
print(labels)"""),

    (34, "Nested comprehension (matrix)", "Intermediate",
     "Nested comprehensions build 2D structures or flatten nested data.",
     """table = [[i*j for j in range(1,6)] for i in range(1,6)]
for row in table:
    print(row)"""),

    (35, "map() with lists", "Intermediate",
     "map(fn, lst) applies fn to every element; wrap in list() to materialise.",
     """nums = [1,2,3,4,5]
doubled  = list(map(lambda x: x*2, nums))
str_nums = list(map(str, nums))
print(doubled)
print(str_nums)"""),

    (36, "filter() with lists", "Intermediate",
     "filter(fn, lst) keeps elements where fn(x) is True.",
     """nums = list(range(-5, 6))
positives = list(filter(lambda x: x > 0, nums))
print(positives)
# Remove falsy values
mixed = [0, 1, '', 'hello', None, [], [1]]
truthy = list(filter(None, mixed))
print(truthy)"""),

    (37, "zip() — combine lists", "Intermediate",
     "zip() pairs corresponding elements; unzip with zip(*pairs).",
     """names  = ['Alice','Bob','Carol']
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f'{name}: {score}')

# Unzip
pairs = list(zip(names, scores))
n2, s2 = zip(*pairs)
print(list(n2), list(s2))"""),

    (38, "enumerate() with start", "Intermediate",
     "enumerate() adds a counter to an iterable. start= sets the first index.",
     """menu = ['Pizza','Burger','Pasta','Salad']
for i, item in enumerate(menu, start=1):
    print(f'{i}. {item}')
# Build index dict
idx = {item: i for i, item in enumerate(menu)}
print(idx)"""),

    (39, "Slice assignment", "Intermediate",
     "Assign to a slice to replace, insert, or delete a range of elements.",
     """lst = [1,2,3,4,5]
lst[1:3] = [20, 30]     # replace indices 1,2
print(lst)
lst[::2] = [0, 0, 0]    # replace every 2nd
print(lst)
lst[1:3] = []            # delete slice
print(lst)"""),

    (40, "Find all indices of a value", "Intermediate",
     "list.index() finds only the first. Use comprehension for all positions.",
     """lst = [1,2,3,2,4,2,5]
target = 2
indices = [i for i, x in enumerate(lst) if x == target]
print(f'Value {target} at indices: {indices}')"""),

    (41, "Rotate a list", "Intermediate",
     "Rotate left or right by splitting and recombining slices.",
     """def rotate_left(lst, n):
    n %= len(lst)
    return lst[n:] + lst[:n]

def rotate_right(lst, n):
    n %= len(lst)
    return lst[-n:] + lst[:-n]

lst = [1,2,3,4,5]
print(rotate_left(lst, 2))    # [3,4,5,1,2]
print(rotate_right(lst, 2))   # [4,5,1,2,3]"""),

    (42, "Chunk a list", "Intermediate",
     "Split into equal-sized sub-lists (last chunk may be smaller).",
     """def chunk(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size)]

lst = list(range(1, 14))
print(chunk(lst, 4))
print(chunk(lst, 5))"""),

    (43, "Transpose a matrix", "Intermediate",
     "zip(*matrix) swaps rows and columns efficiently.",
     """matrix = [[1,2,3],[4,5,6],[7,8,9]]
transposed = [list(row) for row in zip(*matrix)]
for row in transposed:
    print(row)"""),

    (44, "Set operations on lists", "Intermediate",
     "Compute intersection, union, and difference preserving list order.",
     """a = [1,2,3,4,5]
b = [3,4,5,6,7]
inter = [x for x in a if x in b]
diff  = [x for x in a if x not in b]
union = a + [x for x in b if x not in a]
print('Intersection:', inter)
print('Difference:', diff)
print('Union:', union)"""),

    (45, "Flatten deeply nested list", "Intermediate",
     "Recursive function flattens arbitrarily nested lists.",
     """def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

nested = [1, [2, [3, [4, [5]]]], 6]
print(flatten(nested))   # [1,2,3,4,5,6]"""),

    (46, "Running total (cumulative sum)", "Intermediate",
     "itertools.accumulate builds a cumulative sum list.",
     """from itertools import accumulate
nums = [1, 2, 3, 4, 5]
print(list(accumulate(nums)))          # [1,3,6,10,15]
print(list(accumulate(nums, max)))     # running max"""),

    (47, "Moving average", "Intermediate",
     "Compute the average over a sliding window of size k.",
     """def moving_avg(lst, k):
    return [round(sum(lst[i:i+k])/k, 2) for i in range(len(lst)-k+1)]

prices = [10, 12, 11, 13, 15, 14, 16, 18]
print(moving_avg(prices, 3))"""),

    (48, "Group items by key", "Intermediate",
     "Use defaultdict(list) to group items by a key function.",
     """from collections import defaultdict
words = ['apple','ant','banana','bear','cherry','cat']
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)
for letter, grp in sorted(groups.items()):
    print(f'{letter}: {grp}')"""),

    (49, "Counter — most common", "Intermediate",
     "collections.Counter counts occurrences and ranks them.",
     """from collections import Counter
nums = [1,2,3,2,1,2,3,3,2,1,2]
c = Counter(nums)
print(c.most_common(3))
print(dict(c))"""),

    (50, "Binary search (bisect)", "Intermediate",
     "bisect module provides O(log n) insertion-point search on sorted lists.",
     """import bisect
sl = [1,3,5,7,9,11]
print(bisect.bisect_left(sl, 7))    # 3
bisect.insort(sl, 6)                # insert maintaining order
print(sl)"""),

    (51, "Two-pointer technique", "Intermediate",
     "Move two indices toward each other to find pairs summing to a target.",
     """def two_sum(lst, target):
    left, right = 0, len(lst)-1
    while left < right:
        s = lst[left] + lst[right]
        if s == target:   return (lst[left], lst[right])
        elif s < target:  left += 1
        else:             right -= 1
    return None

print(two_sum(sorted([1,2,3,4,6,8,11]), 10))  # (2,8)"""),

    (52, "Sliding window maximum", "Intermediate",
     "Monotonic deque gives O(n) max in each window of size k.",
     """from collections import deque
def sliding_max(lst, k):
    dq, result = deque(), []
    for i, val in enumerate(lst):
        while dq and lst[dq[-1]] <= val:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(lst[dq[0]])
    return result

print(sliding_max([1,3,-1,-3,5,3,6,7], 3))"""),

    (53, "Merge two sorted lists", "Intermediate",
     "Merge in O(n+m) using two pointers.",
     """def merge_sorted(a, b):
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]

print(merge_sorted([1,3,5,7],[2,4,6,8]))"""),

    (54, "Frequency histogram (text)", "Intermediate",
     "Build a simple text histogram from a list of values.",
     """from collections import Counter
data = [1,2,3,2,1,2,3,3,2,1,2,4]
counts = Counter(data)
for val in sorted(counts):
    print(f'{val} | {"█"*counts[val]} ({counts[val]})')"""),

    (55, "Partition list", "Intermediate",
     "Split a list into two sub-lists based on a predicate.",
     """def partition(lst, pred):
    return ([x for x in lst if pred(x)],
            [x for x in lst if not pred(x)])

pos, non_pos = partition(range(-5, 6), lambda x: x > 0)
print('Positive:', pos)
print('Non-positive:', non_pos)"""),

    (56, "Paginate a list", "Intermediate",
     "Return a specific page of items from a list.",
     """def paginate(lst, size, page):
    start = (page-1)*size
    return lst[start:start+size]

data = list(range(1, 26))
for p in range(1, 4):
    print(f'Page {p}: {paginate(data, 8, p)}')"""),

    (57, "Cartesian product", "Intermediate",
     "itertools.product generates all combinations from multiple lists.",
     """from itertools import product as iproduct
colors = ['red','blue']
sizes  = ['S','M','L']
for combo in iproduct(colors, sizes):
    print(combo)"""),

    (58, "Permutations of a list", "Intermediate",
     "itertools.permutations generates all orderings.",
     """from itertools import permutations
lst = [1,2,3]
perms = list(permutations(lst))
print(f'{len(perms)} permutations:')
for p in perms:
    print(p)"""),

    (59, "Combinations of a list", "Intermediate",
     "itertools.combinations generates all r-sized subsets.",
     """from itertools import combinations
team = ['Alice','Bob','Carol','Dave']
print('Pairs:')
for pair in combinations(team, 2):
    print(pair)"""),

    (60, "Interleave two lists", "Intermediate",
     "Alternate elements from two lists into one combined list.",
     """def interleave(a, b):
    result = []
    for pair in zip(a, b):
        result.extend(pair)
    result.extend(a[len(b):] or b[len(a):])
    return result

print(interleave([1,3,5],[2,4,6,8]))"""),

    (61, "Matrix multiplication", "Intermediate",
     "Pure-Python matrix multiply using nested comprehension.",
     """def mat_mul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))]
            for i in range(len(A))]

A=[[1,2],[3,4]]; B=[[5,6],[7,8]]
for row in mat_mul(A, B):
    print(row)"""),

    (62, "Max subarray (Kadane's)", "Intermediate",
     "Find the contiguous subarray with the largest sum in O(n).",
     """def max_subarray(lst):
    max_s = cur_s = lst[0]
    for x in lst[1:]:
        cur_s = max(x, cur_s + x)
        max_s = max(max_s, cur_s)
    return max_s

print(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))  # 6"""),

    (63, "Longest increasing subsequence", "Intermediate",
     "Dynamic programming finds the length of the LIS in O(n²).",
     """def lis_len(lst):
    dp = [1]*len(lst)
    for i in range(1,len(lst)):
        for j in range(i):
            if lst[j] < lst[i]:
                dp[i] = max(dp[i], dp[j]+1)
    return max(dp)

print(lis_len([10,9,2,5,3,7,101,18]))  # 4"""),

    (64, "Bubble sort", "Intermediate",
     "Simple O(n²) comparison sort implemented on a list.",
     """def bubble_sort(lst):
    arr = lst[:]
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64,34,25,12,22,11,90]))"""),

    (65, "Merge sort", "Intermediate",
     "Divide-and-conquer O(n log n) sort on a list.",
     """def merge_sort(lst):
    if len(lst)<=1: return lst
    mid = len(lst)//2
    L,R = merge_sort(lst[:mid]), merge_sort(lst[mid:])
    res,i,j = [],0,0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: res.append(L[i]); i+=1
        else:           res.append(R[j]); j+=1
    return res+L[i:]+R[j:]

print(merge_sort([38,27,43,3,9,82,10]))"""),

    (66, "Quick sort", "Intermediate",
     "Pivot-based sort. Average O(n log n); worst O(n²).",
     """def quick_sort(lst):
    if len(lst)<=1: return lst
    p = lst[len(lst)//2]
    L = [x for x in lst if x < p]
    M = [x for x in lst if x == p]
    R = [x for x in lst if x > p]
    return quick_sort(L)+M+quick_sort(R)

print(quick_sort([3,6,8,10,1,2,1]))"""),

    (67, "Priority queue with heapq", "Intermediate",
     "heapq provides O(log n) push/pop on a plain list used as a min-heap.",
     """import heapq
tasks = []
heapq.heappush(tasks, (3,'low priority'))
heapq.heappush(tasks, (1,'urgent'))
heapq.heappush(tasks, (2,'normal'))
while tasks:
    pri, task = heapq.heappop(tasks)
    print(f'[{pri}] {task}')"""),

    (68, "Counting sort", "Intermediate",
     "O(n+k) integer sort: count occurrences, then reconstruct.",
     """def counting_sort(lst):
    lo,hi = min(lst),max(lst)
    cnt = [0]*(hi-lo+1)
    for v in lst: cnt[v-lo]+=1
    return [i+lo for i,c in enumerate(cnt) for _ in range(c)]

print(counting_sort([4,2,2,8,3,3,1]))"""),

    (69, "Radix sort", "Intermediate",
     "Sort integers digit by digit using counting sort as subroutine.",
     """def radix_sort(lst):
    maxv = max(lst); exp = 1
    while maxv//exp > 0:
        buckets = [[] for _ in range(10)]
        for n in lst: buckets[(n//exp)%10].append(n)
        lst = [n for b in buckets for n in b]
        exp *= 10
    return lst

print(radix_sort([170,45,75,90,802,24,2,66]))"""),

    (70, "Topological sort", "Intermediate",
     "DFS-based topological ordering of a DAG represented as an adjacency list.",
     """def topo_sort(graph):
    visited, stack = set(), []
    def dfs(n):
        visited.add(n)
        for nb in graph.get(n,[]):
            if nb not in visited: dfs(nb)
        stack.append(n)
    for n in list(graph):
        if n not in visited: dfs(n)
    return stack[::-1]

g = {5:[2,0],4:[0,1],2:[3],3:[1],0:[],1:[]}
print(topo_sort(g))"""),

    # ── ADVANCED 71-100 ──
    (71, "Custom list subclass", "Advanced",
     "Subclass list to add validation, logging, or domain-specific behaviour.",
     """class BoundedList(list):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size
    def append(self, item):
        if len(self) >= self.max_size:
            raise OverflowError(f'Max {self.max_size} reached')
        super().append(item)

b = BoundedList(3)
b.append(1); b.append(2); b.append(3)
try:    b.append(4)
except OverflowError as e: print(e)"""),

    (72, "Immutable FrozenList", "Advanced",
     "Wrap a list to block all mutations, raising TypeError on any write.",
     """class FrozenList:
    def __init__(self, data):
        object.__setattr__(self, '_d', list(data))
    def __getitem__(self, i): return self._d[i]
    def __len__(self):        return len(self._d)
    def __iter__(self):       return iter(self._d)
    def __setitem__(self, i, v): raise TypeError('FrozenList is immutable')
    def __repr__(self): return f'FrozenList({self._d})'

fl = FrozenList([1,2,3])
print(fl[1])
try:    fl[0]=99
except TypeError as e: print(e)"""),

    (73, "Lazy list (custom iterator)", "Advanced",
     "A class that generates values on demand via __iter__ / __next__.",
     """class LazyRange:
    def __init__(self, start, stop, step=1):
        self.start,self.stop,self.step = start,stop,step
    def __iter__(self):
        n=self.start
        while n<self.stop:
            yield n; n+=self.step
    def __len__(self):
        return max(0,(self.stop-self.start+self.step-1)//self.step)

lr = LazyRange(0,10,2)
print(list(lr))
print(len(lr))"""),

    (74, "Doubly linked list", "Advanced",
     "O(1) insert/delete at both ends using prev/next node pointers.",
     """class Node:
    __slots__=('val','prev','next')
    def __init__(self,v): self.val=v; self.prev=self.next=None

class DLL:
    def __init__(self): self.head=self.tail=None
    def push_back(self,v):
        n=Node(v)
        if not self.tail: self.head=self.tail=n
        else: n.prev=self.tail; self.tail.next=n; self.tail=n
    def to_list(self):
        r,c=[],self.head
        while c: r.append(c.val); c=c.next
        return r

d=DLL()
for v in [1,2,3,4,5]: d.push_back(v)
print(d.to_list())"""),

    (75, "Sparse list", "Advanced",
     "Store only non-default values in a dict; behaves like a huge list.",
     """class SparseList:
    def __init__(self,size,default=0):
        self.size=size; self.default=default; self._d={}
    def __getitem__(self,i): return self._d.get(i,self.default)
    def __setitem__(self,i,v):
        if v==self.default: self._d.pop(i,None)
        else: self._d[i]=v
    def __len__(self): return self.size

sl=SparseList(1_000_000)
sl[999_999]=42
print(sl[999_999],sl[0],len(sl._d))"""),

    (76, "Segment tree (range sum)", "Advanced",
     "O(log n) range sum queries and point updates on a list.",
     """class SegTree:
    def __init__(self,lst):
        self.n=len(lst); self.t=[0]*(2*self.n)
        for i,v in enumerate(lst): self.t[self.n+i]=v
        for i in range(self.n-1,0,-1): self.t[i]=self.t[2*i]+self.t[2*i+1]
    def update(self,i,v):
        i+=self.n; self.t[i]=v
        while i>1: i//=2; self.t[i]=self.t[2*i]+self.t[2*i+1]
    def query(self,l,r):
        l+=self.n; r+=self.n; s=0
        while l<r:
            if l&1: s+=self.t[l]; l+=1
            if r&1: r-=1; s+=self.t[r]
            l>>=1; r>>=1
        return s

st=SegTree([1,3,5,7,9,11])
print(st.query(1,4))  # 15
st.update(2,10)
print(st.query(1,4))  # 20"""),

    (77, "Fenwick tree (BIT)", "Advanced",
     "Binary Indexed Tree for O(log n) prefix sums over a list.",
     """class BIT:
    def __init__(self,n): self.n=n; self.t=[0]*(n+1)
    def update(self,i,d):
        while i<=self.n: self.t[i]+=d; i+=i&(-i)
    def query(self,i):
        s=0
        while i>0: s+=self.t[i]; i-=i&(-i)
        return s
    def range_q(self,l,r): return self.query(r)-self.query(l-1)

bit=BIT(10)
for i,v in enumerate(range(1,11),1): bit.update(i,v)
print(bit.range_q(3,7))  # 25"""),

    (78, "Monotonic stack (next greater)", "Advanced",
     "A stack maintaining decreasing order to find the next greater element in O(n).",
     """def next_greater(lst):
    n=len(lst); result=[-1]*n; stack=[]
    for i,v in enumerate(lst):
        while stack and lst[stack[-1]]<v:
            result[stack.pop()]=v
        stack.append(i)
    return result

print(next_greater([4,5,2,10,8]))  # [5,10,10,-1,-1]"""),

    (79, "Circular buffer", "Advanced",
     "Fixed-size ring buffer with O(1) writes, ideal for streaming windows.",
     """class CircBuf:
    def __init__(self,size):
        self.buf=[None]*size; self.size=size; self.head=self.cnt=0
    def write(self,v):
        self.buf[self.head%self.size]=v
        self.head+=1; self.cnt=min(self.cnt+1,self.size)
    def read(self):
        s=(self.head-self.cnt)%self.size
        return [self.buf[(s+i)%self.size] for i in range(self.cnt)]

cb=CircBuf(4)
for v in range(1,7): cb.write(v)
print(cb.read())  # [3,4,5,6]"""),

    (80, "Difference array (range updates)", "Advanced",
     "Apply +val to lst[l..r] in O(1); reconstruct in O(n).",
     """def range_add(n, ops):
    diff=[0]*(n+1)
    for l,r,v in ops: diff[l]+=v; diff[r+1]-=v
    cur=0; result=[]
    for d in diff[:n]: cur+=d; result.append(cur)
    return result

print(range_add(6,[(1,3,2),(2,4,3),(0,2,1)]))"""),

    (81, "LRU cache on a list", "Advanced",
     "Least-Recently-Used eviction using OrderedDict as an ordered list.",
     """from collections import OrderedDict
class LRUCache:
    def __init__(self,cap): self.cap=cap; self.c=OrderedDict()
    def get(self,k):
        if k not in self.c: return -1
        self.c.move_to_end(k); return self.c[k]
    def put(self,k,v):
        if k in self.c: self.c.move_to_end(k)
        self.c[k]=v
        if len(self.c)>self.cap: self.c.popitem(last=False)

lru=LRUCache(2)
lru.put(1,'a'); lru.put(2,'b')
print(lru.get(1))   # 'a'
lru.put(3,'c')
print(lru.get(2))   # -1"""),

    (82, "K-way merge (heapq)", "Advanced",
     "Merge k sorted lists into one sorted list using a min-heap in O(n log k).",
     """import heapq
def k_merge(lists):
    heap=[]; iters=[iter(l) for l in lists]
    for i,it in enumerate(iters):
        v=next(it,None)
        if v is not None: heapq.heappush(heap,(v,i))
    result=[]
    while heap:
        v,i=heapq.heappop(heap); result.append(v)
        nxt=next(iters[i],None)
        if nxt is not None: heapq.heappush(heap,(nxt,i))
    return result

print(k_merge([[1,4,7],[2,5,8],[3,6,9]]))"""),

    (83, "Reservoir sampling", "Advanced",
     "Randomly select k items from a list in one pass (streaming algorithm).",
     """import random
def reservoir(stream, k):
    res=stream[:k]
    for i in range(k,len(stream)):
        j=random.randint(0,i)
        if j<k: res[j]=stream[i]
    return res

data=list(range(100))
print('Sample:', sorted(reservoir(data,5)))"""),

    (84, "0-1 Knapsack DP (list table)", "Advanced",
     "2D list as DP table for the 0-1 knapsack problem.",
     """def knapsack(wts,vals,W):
    n=len(wts)
    dp=[[0]*(W+1) for _ in range(n+1)]
    for i in range(1,n+1):
        for w in range(W+1):
            dp[i][w]=dp[i-1][w]
            if wts[i-1]<=w:
                dp[i][w]=max(dp[i][w],dp[i-1][w-wts[i-1]]+vals[i-1])
    return dp[n][W]

print(knapsack([2,3,4,5],[3,4,5,6],8))  # 10"""),

    (85, "Trie (list-of-dicts)", "Advanced",
     "Prefix tree built from lists/dicts for O(m) string search.",
     """class Trie:
    def __init__(self): self.root={}
    def insert(self,w):
        n=self.root
        for c in w: n=n.setdefault(c,{})
        n['$']=True
    def search(self,w):
        n=self.root
        for c in w:
            if c not in n: return False
            n=n[c]
        return '$' in n
    def starts_with(self,p):
        n=self.root
        for c in p:
            if c not in n: return False
            n=n[c]
        return True

t=Trie()
for w in ['apple','app','apt','bat']: t.insert(w)
print(t.search('app'))       # True
print(t.starts_with('ap'))   # True
print(t.search('ap'))        # False"""),

    (86, "Sorted multiset (bisect)", "Advanced",
     "Maintain a sorted list with duplicates using bisect for O(log n) ops.",
     """import bisect
class SortedMS:
    def __init__(self): self.d=[]
    def add(self,v): bisect.insort(self.d,v)
    def remove(self,v):
        i=bisect.bisect_left(self.d,v)
        if i<len(self.d) and self.d[i]==v: del self.d[i]
    def min(self): return self.d[0]
    def max(self): return self.d[-1]

ms=SortedMS()
for v in [3,1,4,1,5,9,2,6]: ms.add(v)
print(ms.d)
ms.remove(1); print(ms.d)
print(ms.min(), ms.max())"""),

    (87, "List-based event sourcing", "Advanced",
     "Store every mutation as an event; replay the list to reconstruct state.",
     """class EventStore:
    def __init__(self): self.events=[]; self.bal=0
    def apply(self,ev):
        self.events.append(ev)
        if ev['t']=='dep':  self.bal+=ev['amt']
        elif ev['t']=='wdw': self.bal-=ev['amt']
    def replay(self):
        b=0
        for e in self.events:
            if e['t']=='dep': b+=e['amt']
            else: b-=e['amt']
        return b

es=EventStore()
es.apply({'t':'dep','amt':1000})
es.apply({'t':'wdw','amt':300})
es.apply({'t':'dep','amt':500})
print('Current:', es.bal)
print('Replayed:', es.replay())"""),

    (88, "Polynomial evaluation (Horner)", "Advanced",
     "Evaluate poly with coefficients in a list using Horner's method in O(n).",
     """def poly_eval(coeffs, x):
    r=0
    for c in coeffs: r=r*x+c
    return r

# 3x³+2x²+x+5 at x=2
print(poly_eval([3,2,1,5], 2))   # 39
print(3*8+2*4+1*2+5)             # 39"""),

    (89, "Move-to-front self-organising list", "Advanced",
     "After each access, the element moves to front for adaptive O(1) amortised hits.",
     """class MTFList:
    def __init__(self,data): self.d=list(data)
    def access(self,v):
        try:
            i=self.d.index(v); self.d.pop(i); self.d.insert(0,v)
            print(f'"{v}" was at {i} → moved to front')
        except ValueError: print(f'"{v}" not found')
    def __repr__(self): return str(self.d)

m=MTFList(['dog','cat','bird','fish','ant'])
print(m)
m.access('fish'); print(m)
m.access('cat');  print(m)
m.access('fish'); print(m)"""),

    (90, "External merge sort (simulated)", "Advanced",
     "Split list into sorted chunks, then k-way merge — simulates disk-based sort.",
     """import heapq
def ext_sort(lst,chunk):
    runs=[sorted(lst[i:i+chunk]) for i in range(0,len(lst),chunk)]
    heap=[]; iters=[iter(r) for r in runs]
    for i,it in enumerate(iters):
        v=next(it,None)
        if v is not None: heapq.heappush(heap,(v,i))
    result=[]
    while heap:
        v,i=heapq.heappop(heap); result.append(v)
        nxt=next(iters[i],None)
        if nxt is not None: heapq.heappush(heap,(nxt,i))
    return result

import random
data=[random.randint(1,99) for _ in range(20)]
print('Input:', data)
print('Sorted:', ext_sort(data,5))"""),

    (91, "Skip list", "Advanced",
     "Probabilistic sorted data structure with O(log n) average operations.",
     """import random
class _N:
    def __init__(self,v,lvl): self.v=v; self.f=[None]*(lvl+1)
class SkipList:
    MAX=4
    def __init__(self): self.h=_N(float('-inf'),self.MAX); self.lvl=0
    def _rl(self):
        l=0
        while random.random()<0.5 and l<self.MAX: l+=1
        return l
    def insert(self,v):
        upd=[None]*(self.MAX+1); c=self.h
        for i in range(self.lvl,-1,-1):
            while c.f[i] and c.f[i].v<v: c=c.f[i]
            upd[i]=c
        l=self._rl()
        if l>self.lvl:
            for i in range(self.lvl+1,l+1): upd[i]=self.h
            self.lvl=l
        n=_N(v,l)
        for i in range(l+1): n.f[i]=upd[i].f[i]; upd[i].f[i]=n
    def to_list(self):
        r=[]; c=self.h.f[0]
        while c: r.append(c.v); c=c.f[0]
        return r

sl=SkipList()
for v in [3,1,4,1,5,9,2,6]: sl.insert(v)
print(sl.to_list())"""),

    (92, "BFS shortest path on 2D grid list", "Advanced",
     "BFS on a 2D list to find the shortest unobstructed path.",
     """from collections import deque
def bfs_grid(grid,start,end):
    R,C=len(grid),len(grid[0])
    q=deque([(start,0)]); vis={start}
    while q:
        (r,c),d=q.popleft()
        if (r,c)==end: return d
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc]==0 and (nr,nc) not in vis:
                vis.add((nr,nc)); q.append(((nr,nc),d+1))
    return -1

grid=[[0,0,0,0],[1,1,0,1],[0,0,0,0],[0,1,1,0]]
print(bfs_grid(grid,(0,0),(3,3)))"""),

    (93, "Bit set using list of ints", "Advanced",
     "Compact bitset using a list of 64-bit integers for Boolean flags.",
     """class BitSet:
    def __init__(self,n): self.d=[0]*((n+63)//64)
    def set(self,i):   self.d[i//64]|= 1<<(i%64)
    def get(self,i):   return bool(self.d[i//64]&(1<<(i%64)))
    def clear(self,i): self.d[i//64]&=~(1<<(i%64))

bs=BitSet(200)
bs.set(100); bs.set(150)
print(bs.get(100))   # True
print(bs.get(50))    # False
bs.clear(100)
print(bs.get(100))   # False"""),

    (94, "Zipper (focus + context)", "Advanced",
     "A zipper splits a list at a focus point for O(1) local edits.",
     """class Zipper:
    def __init__(self,lst,pos=0):
        self.left=lst[:pos]; self.right=lst[pos:]
    def right_(self):
        if self.right: self.left.append(self.right.pop(0))
    def left_(self):
        if self.left: self.right.insert(0,self.left.pop())
    def insert(self,v): self.right.insert(0,v)
    @property
    def focus(self): return self.right[0] if self.right else None
    def to_list(self): return self.left+self.right

z=Zipper([1,2,3,4,5],pos=2)
print('Focus:',z.focus)
z.insert(99); print(z.to_list())
z.right_(); print('Focus:',z.focus)"""),

    (95, "Persistent list (structural sharing)", "Advanced",
     "Prepend in O(1) by sharing the tail — functional/immutable style.",
     """class _PNode:
    __slots__=('v','n')
    def __init__(self,v,n=None): self.v=v; self.n=n

def to_plist(lst):
    h=None
    for v in reversed(lst): h=_PNode(v,h)
    return h

def prepend(node,v): return _PNode(v,node)

def to_pylist(node):
    r=[]
    while node: r.append(node.v); node=node.n
    return r

v1=to_plist([1,2,3])
v2=prepend(v1,0)        # shares v1 nodes
print(to_pylist(v1))    # [1,2,3]
print(to_pylist(v2))    # [0,1,2,3]"""),

    (96, "Wavelet transform (prefix lists)", "Advanced",
     "Frequency analysis using prefix sums stored in lists.",
     """def prefix_sum(lst):
    p=[0]*(len(lst)+1)
    for i,v in enumerate(lst): p[i+1]=p[i]+v
    return p

def range_sum(prefix,l,r):    # sum in [l,r]
    return prefix[r+1]-prefix[l]

data=[3,1,4,1,5,9,2,6,5,3]
ps=prefix_sum(data)
print('Array:',data)
print('Sum [2..6]:',range_sum(ps,2,6))   # 4+1+5+9+2=21
print('Sum [0..4]:',range_sum(ps,0,4))   # 3+1+4+1+5=14"""),

    (97, "List-based state machine", "Advanced",
     "Use a list of states and a dict transition table to model a finite automaton.",
     """STATES=['idle','running','paused','stopped']
TRANS={('idle','start'):'running',('running','pause'):'paused',
       ('running','stop'):'stopped',('paused','resume'):'running',
       ('paused','stop'):'stopped'}

state='idle'
for event in ['start','pause','resume','stop']:
    nxt=TRANS.get((state,event))
    if nxt: print(f'{state} --{event}--> {nxt}'); state=nxt
    else: print(f'Invalid: {event} in state {state}')"""),

    (98, "Convex hull (Graham scan)", "Advanced",
     "Find the convex hull of 2D points using a list as a stack.",
     """import math
def convex_hull(pts):
    pts=sorted(set(pts))
    if len(pts)<=1: return pts
    def cross(O,A,B):
        return (A[0]-O[0])*(B[1]-O[1])-(A[1]-O[1])*(B[0]-O[0])
    lower=[]
    for p in pts:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0: lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(pts):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0: upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]

pts=[(0,0),(1,1),(2,2),(0,2),(2,0),(1,0),(0,1)]
print(convex_hull(pts))"""),

    (99, "List-based mini interpreter", "Advanced",
     "Recursive descent parser that evaluates arithmetic from a list of tokens.",
     """class Interpreter:
    def __init__(self,text): self.t=text.replace(' ',''); self.pos=0
    def peek(self): return self.t[self.pos] if self.pos<len(self.t) else None
    def eat(self,c): assert self.peek()==c; self.pos+=1
    def num(self):
        s=self.pos
        while self.peek() and self.peek().isdigit(): self.pos+=1
        return int(self.t[s:self.pos])
    def factor(self):
        if self.peek()=='(':
            self.eat('('); v=self.expr(); self.eat(')'); return v
        return self.num()
    def term(self):
        v=self.factor()
        while self.peek() in ('*','/'):
            op=self.peek(); self.pos+=1
            v=v*self.factor() if op=='*' else v//self.factor()
        return v
    def expr(self):
        v=self.term()
        while self.peek() in ('+','-'):
            op=self.peek(); self.pos+=1
            v=v+self.term() if op=='+' else v-self.term()
        return v

for e in ['3+4*2','(3+4)*2','100-25*3+7']:
    print(f'{e} = {Interpreter(e).expr()}')"""),

    (100, "Conway's Game of Life on a 2D list", "Advanced",
     "Classic cellular automaton: each cell's survival depends on its list neighbours.",
     """def gol_step(grid):
    R,C=len(grid),len(grid[0])
    def neighbours(r,c):
        return sum(grid[r+dr][c+dc]
                   for dr in [-1,0,1] for dc in [-1,0,1]
                   if (dr,dc)!=(0,0) and 0<=r+dr<R and 0<=c+dc<C)
    return [[1 if (grid[r][c] and neighbours(r,c) in (2,3))
               or (not grid[r][c] and neighbours(r,c)==3)
               else 0
             for c in range(C)] for r in range(R)]

def show(g): return '\\n'.join(' '.join('█' if c else '.' for c in r) for r in g)

# Blinker oscillator
grid=[[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0]]
print('Gen 0:'); print(show(grid))
grid=gol_step(grid)
print('\\nGen 1:'); print(show(grid))"""),
]

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🐍 List Reference")
    section = st.radio("Navigate to", [
        "🏠 Overview",
        "📚 All List Methods",
        "🔧 Built-in Functions",
        "🟢 Beginner (1–30)",
        "🔵 Intermediate (31–70)",
        "🟣 Advanced (71–100)",
        "🎮 Interactive Playground",
        "📊 Visual Explorer",
    ])
    st.markdown("---")
    st.markdown("**Quick Stats**")
    st.markdown("• 11 list methods")
    st.markdown("• 17 built-in functions")
    st.markdown("• 100 code examples")
    st.markdown("• Beginner → Advanced")

# ──────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
  <h1>🐍 Python LIST — Complete Reference</h1>
  <p>All Methods · All Built-in Functions · 100 Code Examples · Beginner → Advanced</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# OVERVIEW
# ──────────────────────────────────────────────────────────────
if section == "🏠 Overview":
    st.markdown("""
<div class='stat-row'>
  <div class='stat-box'><div class='stat-num'>11</div><div class='stat-lbl'>List Methods</div></div>
  <div class='stat-box'><div class='stat-num'>17</div><div class='stat-lbl'>Built-in Functions</div></div>
  <div class='stat-box'><div class='stat-num'>100</div><div class='stat-lbl'>Code Examples</div></div>
  <div class='stat-box'><div class='stat-num'>3</div><div class='stat-lbl'>Difficulty Levels</div></div>
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📖 What is a Python List?")
        st.markdown("""
A **list** is Python's most versatile built-in data structure.

| Property | Value |
|---|---|
| Ordered | ✅ Yes |
| Mutable | ✅ Yes |
| Duplicates | ✅ Allowed |
| Heterogeneous | ✅ Any mix of types |
| Indexed | ✅ Zero-based |
| Sliceable | ✅ `lst[start:stop:step]` |

```python
# Create a list
my_list = [1, "hello", 3.14, True, [1,2]]
```
""")
    with c2:
        st.markdown("### 🗂️ What's Inside This App?")
        st.markdown("""
| Section | Contents |
|---|---|
| 📚 All List Methods | `append`, `extend`, `insert`, `remove`, `pop`, `clear`, `index`, `count`, `sort`, `reverse`, `copy` |
| 🔧 Built-in Functions | `len`, `max`, `min`, `sum`, `sorted`, `reversed`, `zip`, `map`, `filter` + more |
| 🟢 Beginner | Creation, indexing, slicing, basic ops (1–30) |
| 🔵 Intermediate | Comprehensions, algorithms, sorting (31–70) |
| 🟣 Advanced | Custom classes, trees, DP, interpreters (71–100) |
| 🎮 Playground | Try any list operation live |
| 📊 Explorer | Visualise list operations |
""")

    st.markdown("### ⚡ Quick Cheatsheet")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code("""# Creation
lst = [1, 2, 3]
lst = list(range(5))
lst = [x**2 for x in range(5)]""", language="python")
    with col2:
        st.code("""# Access & Modify
lst[0]       # first
lst[-1]      # last
lst[1:3]     # slice
lst[i] = v   # update""", language="python")
    with col3:
        st.code("""# Common ops
lst.append(x)
lst.sort()
lst.reverse()
len(lst)
x in lst""", language="python")

# ──────────────────────────────────────────────────────────────
# ALL LIST METHODS
# ──────────────────────────────────────────────────────────────
elif section == "📚 All List Methods":
    st.markdown("<div class='sec-header'>📚 All 11 Built-in List Methods</div>", unsafe_allow_html=True)
    for m in LIST_METHODS:
        with st.expander(f"🔹 `{m['name']}` — {m['time']}", expanded=False):
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown(f"**Definition:** {m['definition']}")
                st.markdown(f"**Syntax:** `{m['syntax']}`")
                st.info(f"💡 {m['tip']}")
            with c2:
                st.code(m["example"], language="python")

# ──────────────────────────────────────────────────────────────
# BUILT-IN FUNCTIONS
# ──────────────────────────────────────────────────────────────
elif section == "🔧 Built-in Functions":
    st.markdown("<div class='sec-header'>🔧 17 Built-in Functions That Work With Lists</div>", unsafe_allow_html=True)
    for fn in BUILTIN_FUNCTIONS:
        st.markdown(f"""
<div class='card'>
  <div class='card-title'><code>{fn['name']}</code></div>
  <div class='card-def'>{fn['definition']}</div>
  <div class='card-syntax'>{fn['example']}</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# EXAMPLE SECTIONS
# ──────────────────────────────────────────────────────────────
elif section in ("🟢 Beginner (1–30)", "🔵 Intermediate (31–70)", "🟣 Advanced (71–100)"):
    level_map = {
        "🟢 Beginner (1–30)":       ("Beginner",     "🟢", "badge-beg"),
        "🔵 Intermediate (31–70)":  ("Intermediate", "🔵", "badge-int"),
        "🟣 Advanced (71–100)":     ("Advanced",     "🟣", "badge-adv"),
    }
    level_name, emoji, badge_cls = level_map[section]

    filtered = [(n, t, l, d, c) for n, t, l, d, c in EXAMPLES if l == level_name]

    st.markdown(
        f"<div class='sec-header'>{emoji} {level_name} — {len(filtered)} Examples</div>",
        unsafe_allow_html=True,
    )

    search = st.text_input("🔍 Search examples by title or keyword", "")

    for num, title, level, defn, code_src in filtered:
        if search and search.lower() not in title.lower() and search.lower() not in code_src.lower():
            continue
        with st.expander(f"#{num} — {title}", expanded=False):
            st.markdown(f"<span class='{badge_cls}'>{level}</span>", unsafe_allow_html=True)
            st.markdown(f"**📖 Definition:** {defn}")
            st.code(code_src, language="python")
            if st.button(f"▶ Run Example #{num}", key=f"run_{num}"):
                st.markdown("**Output:**")
                try:
                    import io, contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        exec(code_src, {
                            "__builtins__": __builtins__,
                            "random": random, "time": time,
                            "math": math, "copy": copy,
                            "bisect": bisect, "heapq": heapq,
                            "Counter": Counter, "defaultdict": defaultdict,
                            "deque": deque, "OrderedDict": OrderedDict,
                            "accumulate": accumulate, "chain": chain,
                            "combinations": combinations,
                            "permutations": permutations,
                            "iproduct": iproduct, "reduce": reduce,
                        })
                    out = buf.getvalue()
                    st.markdown(f"<div class='out-box'>{out if out else '(no output)'}</div>",
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# ──────────────────────────────────────────────────────────────
# INTERACTIVE PLAYGROUND
# ──────────────────────────────────────────────────────────────
elif section == "🎮 Interactive Playground":
    st.markdown("<div class='sec-header'>🎮 Interactive List Playground</div>", unsafe_allow_html=True)

    st.markdown("### 🧪 Live List Builder")
    c1, c2 = st.columns(2)
    with c1:
        raw = st.text_input("Enter list values (comma-separated)", "3, 1, 4, 1, 5, 9, 2, 6, 5, 3")
        try:
            lst = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except:
            lst = [int(x) for x in raw.replace(","," ").split() if x.isdigit()]

        method = st.selectbox("Choose a list method", [
            "append(x)", "extend([x,y])", "insert(i,x)", "remove(x)",
            "pop()", "pop(i)", "clear()", "index(x)", "count(x)",
            "sort()", "sort(reverse=True)", "reverse()", "copy()",
        ])
        param = st.text_input("Parameter (x or i,x):", "99")

    with c2:
        st.markdown(f"**Current list:** `{lst}`")
        if st.button("▶ Apply Method"):
            result_lst = lst[:]
            output = ""
            try:
                if method == "append(x)":
                    result_lst.append(int(param)); output = str(result_lst)
                elif method == "extend([x,y])":
                    vals = [int(v.strip()) for v in param.split(",")]
                    result_lst.extend(vals); output = str(result_lst)
                elif method == "insert(i,x)":
                    i, v = map(int, param.split(","))
                    result_lst.insert(i, v); output = str(result_lst)
                elif method == "remove(x)":
                    result_lst.remove(int(param)); output = str(result_lst)
                elif method == "pop()":
                    popped = result_lst.pop(); output = f"Popped: {popped}\nList: {result_lst}"
                elif method == "pop(i)":
                    popped = result_lst.pop(int(param)); output = f"Popped: {popped}\nList: {result_lst}"
                elif method == "clear()":
                    result_lst.clear(); output = str(result_lst)
                elif method == "index(x)":
                    output = f"Index of {param}: {result_lst.index(int(param))}"
                elif method == "count(x)":
                    output = f"Count of {param}: {result_lst.count(int(param))}"
                elif method == "sort()":
                    result_lst.sort(); output = str(result_lst)
                elif method == "sort(reverse=True)":
                    result_lst.sort(reverse=True); output = str(result_lst)
                elif method == "reverse()":
                    result_lst.reverse(); output = str(result_lst)
                elif method == "copy()":
                    output = f"Copy: {result_lst.copy()}"
            except Exception as e:
                output = f"❌ {e}"
            st.markdown(f"<div class='out-box'>{output}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✏️ Free Code Editor")
    default_code = """# Write any Python list code here
lst = [3, 1, 4, 1, 5, 9, 2, 6]

# Sort and display
sorted_lst = sorted(lst)
print("Original:", lst)
print("Sorted:  ", sorted_lst)

# Comprehension
squares = [x**2 for x in lst if x > 3]
print("Squares > 3:", squares)

# Statistics
print(f"Sum: {sum(lst)}, Max: {max(lst)}, Min: {min(lst)}")
"""
    user_code = st.text_area("Python code:", default_code, height=220)
    if st.button("▶ Run Code", type="primary"):
        import io, contextlib
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(user_code, {
                    "__builtins__": __builtins__,
                    "random": random, "math": math, "copy": copy,
                    "bisect": bisect, "heapq": heapq,
                    "Counter": Counter, "defaultdict": defaultdict,
                    "deque": deque, "OrderedDict": OrderedDict,
                    "accumulate": accumulate, "chain": chain,
                    "combinations": combinations, "permutations": permutations,
                    "reduce": reduce,
                })
            st.markdown(f"<div class='out-box'>{buf.getvalue()}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────────────────────
# VISUAL EXPLORER
# ──────────────────────────────────────────────────────────────
elif section == "📊 Visual Explorer":
    st.markdown("<div class='sec-header'>📊 Visual List Explorer</div>", unsafe_allow_html=True)

    raw2 = st.text_input("Enter numbers (comma-separated)", "5, 3, 8, 1, 9, 2, 7, 4, 6")
    try:
        nums = [int(x.strip()) for x in raw2.split(",") if x.strip()]
    except:
        nums = [5,3,8,1,9,2,7,4,6]

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Bar Chart", "🔢 Sorted Views", "📦 Slicing", "🧮 Operations"])

    with tab1:
        import pandas as pd
        df = pd.DataFrame({"Index": list(range(len(nums))), "Value": nums})
        st.bar_chart(df.set_index("Index"))
        st.markdown(f"**List:** `{nums}`")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sum", sum(nums))
        col2.metric("Max", max(nums))
        col3.metric("Min", min(nums))
        col4.metric("Avg", f"{sum(nums)/len(nums):.2f}")

    with tab2:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Original**")
            st.write(nums)
        with c2:
            st.markdown("**Sorted ↑**")
            st.write(sorted(nums))
        with c3:
            st.markdown("**Sorted ↓**")
            st.write(sorted(nums, reverse=True))

        st.markdown("**Reversed**")
        st.write(nums[::-1])

    with tab3:
        start = st.slider("Start index", 0, len(nums)-1, 0)
        stop  = st.slider("Stop index",  1, len(nums),   len(nums)//2)
        step  = st.slider("Step",        1, 4,           1)
        sliced = nums[start:stop:step]
        st.markdown(f"**`lst[{start}:{stop}:{step}]`** = `{sliced}`")
        if sliced:
            import pandas as pd
            df_s = pd.DataFrame({"Index": list(range(len(sliced))), "Value": sliced})
            st.bar_chart(df_s.set_index("Index"))

    with tab4:
        op = st.selectbox("Operation", [
            "Cumulative Sum", "Running Max", "Running Min",
            "Enumerate pairs", "Zip with index", "Count each value",
        ])
        if op == "Cumulative Sum":
            result = list(accumulate(nums))
            st.write(result)
            import pandas as pd
            st.line_chart(pd.DataFrame({"Cumulative Sum": result}))
        elif op == "Running Max":
            result = list(accumulate(nums, max))
            st.write(result)
        elif op == "Running Min":
            result = list(accumulate(nums, min))
            st.write(result)
        elif op == "Enumerate pairs":
            st.write(list(enumerate(nums)))
        elif op == "Zip with index":
            st.write(list(zip(range(len(nums)), nums)))
        elif op == "Count each value":
            st.write(dict(Counter(nums)))

# ──────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#666; font-size:0.85rem;'>"
    "🐍 Python List Complete Reference · 11 Methods · 17 Functions · 100 Examples"
    "</p>",
    unsafe_allow_html=True,
)