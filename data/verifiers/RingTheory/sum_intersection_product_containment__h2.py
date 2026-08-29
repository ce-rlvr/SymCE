import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: (I+J)(I \\cap J) is not a subset of IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
            if R is None or I is None or J is None:
                return [False, False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1, h2, neg_q = False, False, False

    # Try to interpret R as an integer n for the ring Z/nZ
    n = None
    if isinstance(R, int) or (hasattr(R, 'is_integer') and R.is_integer):
        n = int(R)
    elif isinstance(R, (set, list, tuple)):
        try:
            R_set = set(R)
            if all(isinstance(x, int) for x in R_set):
                n_candidate = max(R_set) + 1
                if R_set == set(range(n_candidate)):
                    n = n_candidate
        except Exception:
            pass

    if n is not None and 1 <= n <= 1000:
        h1 = True
        try:
            I_set = { int(i) % n for i in I }
            J_set = { int(j) % n for j in J }
        except Exception:
            return [False, False, False]

        if J_set:
            h2 = True
            # Check closure under addition
            for a in J_set:
                for b in J_set:
                    if (a + b) % n not in J_set:
                        h2 = False
                        break
                if not h2: break
            # Check closure under scalar multiplication
            if h2:
                for a in J_set:
                    for r in range(n):
                        if (a * r) % n not in J_set:
                            h2 = False
                            break
                    if not h2: break
        else:
            h2 = False

        try:
            I_plus_J = { (i + j) % n for i in I_set for j in J_set }
            I_cap_J = I_set.intersection(J_set)
            LHS = { (x * y) % n for x in I_plus_J for y in I_cap_J }
            RHS = { (i * j) % n for i in I_set for j in J_set }
            neg_q = not LHS.issubset(RHS)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]

    # Generic finite ring fallback
    if isinstance(R, (set, list, tuple)):
        try:
            R_list = list(R)
            if len(R_list) > 1000:
                return [False, False, False]
                
            I_set = set(I)
            J_set = set(J)

            # Check if R is a commutative ring (commutativity check)
            h1 = True
            for a in R_list:
                for b in R_list:
                    if (a * b) != (b * a):
                        h1 = False
                        break
                if not h1: break

            if h1:
                if J_set and J_set.issubset(set(R_list)):
                    h2 = True
                    for a in J_set:
                        for b in J_set:
                            if (a + b) not in J_set:
                                h2 = False
                                break
                        if not h2: break
                    if h2:
                        for a in J_set:
                            for r in R_list:
                                if (a * r) not in J_set:
                                    h2 = False
                                    break
                            if not h2: break
                else:
                    h2 = False

            if h1 and h2:
                I_plus_J = { (i + j) for i in I_set for j in J_set }
                I_cap_J = I_set.intersection(J_set)
                LHS = { (x * y) for x in I_plus_J for y in I_cap_J }
                RHS = { (i * j) for i in I_set for j in J_set }
                neg_q = not LHS.issubset(RHS)

            return [h1, h2, neg_q]
        except Exception:
            pass

    return [False, False, False]