import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_elements = list(witness['R_elements'])
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            R_zero = witness['R_zero']
            R_one = witness['R_one']
            M_rank = int(witness['M_rank'])
            M_torsion = [int(t) for t in witness['M_torsion']]
            action = witness['action']
        else:
            R_elements = list(witness.R_elements)
            R_add = witness.R_add
            R_mul = witness.R_mul
            R_zero = witness.R_zero
            R_one = witness.R_one
            M_rank = int(witness.M_rank)
            M_torsion = [int(t) for t in witness.M_torsion]
            action = witness.action
            
        if len(R_elements) > 20 or len(R_elements) == 0:
            return [False] * 5
            
        if M_rank + len(M_torsion) > 20:
            return [False] * 5
            
    except Exception:
        return [False] * 5

    # H1: R has a multiplicative identity
    h1 = False
    try:
        if R_one in R_elements and R_zero in R_elements:
            is_ring = True
            
            # Check uniqueness of elements
            for i in range(len(R_elements)):
                for j in range(i + 1, len(R_elements)):
                    if R_elements[i] == R_elements[j]:
                        is_ring = False
                        
            # Check closure, assoc, comm for add
            for a in R_elements:
                for b in R_elements:
                    if R_add(a, b) not in R_elements: is_ring = False
                    if R_mul(a, b) not in R_elements: is_ring = False
                    if R_add(a, b) != R_add(b, a): is_ring = False
                    for c in R_elements:
                        if R_add(R_add(a, b), c) != R_add(a, R_add(b, c)): is_ring = False
                        if R_mul(R_mul(a, b), c) != R_mul(a, R_mul(b, c)): is_ring = False
                        if R_mul(a, R_add(b, c)) != R_add(R_mul(a, b), R_mul(a, c)): is_ring = False
                        if R_mul(R_add(a, b), c) != R_add(R_mul(a, c), R_mul(b, c)): is_ring = False
            
            for a in R_elements:
                if R_add(a, R_zero) != a: is_ring = False
                has_inv = False
                for b in R_elements:
                    if R_add(a, b) == R_zero:
                        has_inv = True
                        break
                if not has_inv: is_ring = False
            
            for a in R_elements:
                if R_mul(a, R_one) != a: is_ring = False
                if R_mul(R_one, a) != a: is_ring = False
            
            h1 = is_ring
    except Exception:
        h1 = False

    # H2: R is a left Artinian ring
    try:
        # Any finite ring is Artinian
        h2 = h1 and isinstance(R_elements, list) and len(R_elements) > 0
    except Exception:
        h2 = False

    # H3: M is a left R-module
    h3 = False
    try:
        if M_rank >= 0 and all(t >= 2 for t in M_torsion):
            N = M_rank + len(M_torsion)
            is_module = True
            zero_M = [0] * N
            
            def reduce_M(x):
                x_list = list(x)
                if len(x_list) != N:
                    raise ValueError("Invalid length")
                res = []
                for i in range(M_rank):
                    res.append(int(x_list[i]))
                for i, t in enumerate(M_torsion):
                    res.append(int(x_list[M_rank + i]) % t)
                return res

            def add_M(x, y):
                return reduce_M([a + b for a, b in zip(x, y)])

            def mul_M(k, x):
                return reduce_M([k * a for a in x])

            def action_extend(r, x):
                res = zero_M
                for i in range(N):
                    if x[i] != 0:
                        term = mul_M(x[i], reduce_M(action(r, i)))
                        res = add_M(res, term)
                return res

            for r in R_elements:
                for s in R_elements:
                    for i in range(N):
                        act_r = reduce_M(action(r, i))
                        act_s = reduce_M(action(s, i))
                        
                        act_r_plus_s = reduce_M(action(R_add(r, s), i))
                        if act_r_plus_s != add_M(act_r, act_s):
                            is_module = False
                        
                        act_rs = reduce_M(action(R_mul(r, s), i))
                        if act_rs != action_extend(r, act_s):
                            is_module = False
            
            for r in R_elements:
                for idx, t in enumerate(M_torsion):
                    i = M_rank + idx
                    act_r = reduce_M(action(r, i))
                    if mul_M(t, act_r) != zero_M:
                        is_module = False
                        
            h3 = is_module
    except Exception:
        h3 = False

    # H4: M is finitely generated
    try:
        # By definition of the witness format, M is generated by N elements.
        h4 = h3 and True
    except Exception:
        h4 = False

    # neg_Q: M is NOT an Artinian module
    try:
        # A finitely generated module over a finite ring is Artinian iff it is finite.
        # M is finite iff M_rank == 0.
        # So M is NOT Artinian iff M_rank > 0.
        neg_q = h3 and (M_rank > 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is a left Artinian ring",
    "H_3: M is a left R-module",
    "H_4: M is finitely generated",
    "¬Q: M is not an Artinian module"
]

N_HYP = 4
NEG_Q_INDEX = 4