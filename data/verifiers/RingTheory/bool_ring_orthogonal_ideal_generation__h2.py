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

def parse_witness(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return None
        R, S = witness
        if not isinstance(R, (list, set, tuple)) or not isinstance(S, (list, set, tuple)):
            return None
        
        if len(R) == 0 or len(R) > 256:
            return None
            
        def make_hashable(x):
            if isinstance(x, (list, tuple)):
                return tuple(make_hashable(i) for i in x)
            if isinstance(x, set):
                return frozenset(make_hashable(i) for i in x)
            if isinstance(x, dict):
                return frozenset((make_hashable(k), make_hashable(v)) for k, v in x.items())
            return x

        R_set = set(make_hashable(x) for x in R)
        S_set = set(make_hashable(x) for x in S)

        # Try sets
        if all(isinstance(x, frozenset) for x in R_set):
            zero = frozenset()
            if zero in R_set:
                add = lambda a, b: a ^ b
                mul = lambda a, b: a & b
                if all(add(a, b) in R_set and mul(a, b) in R_set for a in R_set for b in R_set):
                    return R_set, S_set, zero, add, mul

        # Try bitwise
        try:
            zero = 0
            if zero in R_set:
                add = lambda a, b: a ^ b
                mul = lambda a, b: a & b
                if all(add(a, b) in R_set and mul(a, b) in R_set for a in R_set for b in R_set):
                    return R_set, S_set, zero, add, mul
        except Exception:
            pass

        # Try standard + and *
        try:
            zero = None
            for z in R_set:
                if all((z + x) == x for x in R_set):
                    zero = z
                    break
            if zero is not None:
                add = lambda a, b: a + b
                mul = lambda a, b: a * b
                if all(add(a, b) in R_set and mul(a, b) in R_set for a in R_set for b in R_set):
                    return R_set, S_set, zero, add, mul
        except Exception:
            pass

        # Try custom ^ and &
        try:
            zero = None
            for z in R_set:
                if all((z ^ x) == x for x in R_set):
                    zero = z
                    break
            if zero is not None:
                add = lambda a, b: a ^ b
                mul = lambda a, b: a & b
                if all(add(a, b) in R_set and mul(a, b) in R_set for a in R_set for b in R_set):
                    return R_set, S_set, zero, add, mul
        except Exception:
            pass

        return None
    except Exception:
        return None

def conditions(witness):
    parsed = parse_witness(witness)
    if parsed is None:
        return [False, False]
    
    R_set, S_set, zero, add, mul = parsed
    
    # H1: R is a Boolean ring and S is a subset
    h1 = True
    try:
        if not S_set.issubset(R_set):
            h1 = False
        else:
            # Check Boolean ring axioms
            for a in R_set:
                if add(a, a) != zero:
                    h1 = False
                    break
                if mul(a, a) != a:
                    h1 = False
                    break
                for b in R_set:
                    if add(a, b) != add(b, a):
                        h1 = False
                        break
                    if mul(a, b) != mul(b, a):
                        h1 = False
                        break
                    for c in R_set:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            h1 = False
                            break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)):
                            h1 = False
                            break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            h1 = False
                            break
                if not h1:
                    break
    except Exception:
        h1 = False

    # neg_Q: The ideal generated by S is NOT the principal ideal generated by sum(S)
    neg_q = False
    try:
        if h1:
            # Compute sum of S
            sum_S = zero
            for s in S_set:
                sum_S = add(sum_S, s)
            
            # Ideal generated by S
            ideal_S = set([zero])
            ideal_S.update(S_set)
            for x in S_set:
                for r in R_set:
                    ideal_S.add(mul(r, x))
            
            while True:
                new_elements = set()
                for a in ideal_S:
                    for b in ideal_S:
                        s_ab = add(a, b)
                        if s_ab not in ideal_S:
                            new_elements.add(s_ab)
                if not new_elements:
                    break
                ideal_S.update(new_elements)
                
            # Ideal generated by sum_S
            ideal_sum_S = set([zero, sum_S])
            for r in R_set:
                ideal_sum_S.add(mul(r, sum_S))
                
            while True:
                new_elements = set()
                for a in ideal_sum_S:
                    for b in ideal_sum_S:
                        s_ab = add(a, b)
                        if s_ab not in ideal_sum_S:
                            new_elements.add(s_ab)
                if not new_elements:
                    break
                ideal_sum_S.update(new_elements)
                
            if ideal_S != ideal_sum_S:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring and S is a subset of R",
    "¬Q: The ideal generated by S is NOT the principal ideal generated by the sum of S"
]

N_HYP = 1
NEG_Q_INDEX = 1