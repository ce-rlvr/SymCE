import math
import z3
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def has_solution(a, b, n):
    x = z3.Int('x')
    y = z3.Int('y')
    solver = z3.Solver()
    solver.add(a * x + b * y == n)
    solver.add(x >= 0)
    solver.add(y >= 0)
    return solver.check() == z3.sat

def conditions(witness):
    try:
        # Witness should be a tuple of two integers (a, b)
        if len(witness) != 2:
            return [False, False]
        a = int(witness[0])
        b = int(witness[1])
        if a != witness[0] or b != witness[1]:
            return [False, False]
    except Exception:
        return [False, False]
    
    try:
        h1 = math.gcd(a, b) == 1
    except Exception:
        h1 = False
        
    try:
        target = a * b - a - b
        
        # The conclusion states that `target` is the LARGEST integer with NO non-negative solutions.
        # This means:
        # 1. `target` itself must have NO non-negative solutions.
        # 2. ALL integers > `target` MUST HAVE non-negative solutions.
        #
        # Therefore, the conclusion FAILS (neg_q is True) if:
        # 1. `target` HAS a non-negative solution, OR
        # 2. SOME integer > `target` HAS NO non-negative solution.
        
        neg_q = False
        if has_solution(a, b, target):
            neg_q = True
        else:
            # Check the next few integers. If the set of integers with no solutions is unbounded
            # (e.g., when a and b are negative), we will quickly find an integer > target with no solution.
            for i in range(1, 11):
                if not has_solution(a, b, target + i):
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: the greatest common divisor of a and b is 1",
    "¬Q: The largest integer n for which ax + by = n has no non-negative integer solutions is NOT ab - a - b"
]

N_HYP = 1
NEG_Q_INDEX = 1