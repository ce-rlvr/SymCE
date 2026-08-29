import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
import sympy.abc as abc

# Top-level setup: named object bindings
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

def is_equal(a, b):
    if a == b:
        return True
    try:
        diff = a - b
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
            return True
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        if hasattr(diff, 'expand'):
            diff = diff.expand()
            if diff == 0 or (hasattr(diff, 'is_zero') and diff.is_zero):
                return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    R, S, n = None, None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, n = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'n'):
            R, S, n = witness.R, witness.S, witness.n
        elif isinstance(witness, dict) and 'R' in witness and 'S' in witness and 'n' in witness:
            R, S, n = witness['R'], witness['S'], witness['n']
    except Exception:
        pass

    # H1: S is a multiplicatively closed subset of R
    try:
        if hasattr(witness, 'h1'):
            h1 = bool(witness.h1())
        elif hasattr(witness, 'S_is_multiplicatively_closed'):
            h1 = bool(witness.S_is_multiplicatively_closed())
        elif R is not None and S is not None:
            try:
                if len(S) > 1000 or len(R) > 10000:
                    raise ValueError("Too large for exhaustive search")
            except Exception:
                raise ValueError("Cannot determine size")
            
            h1 = True
            for s in S:
                if not any(is_equal(s, r) for r in R):
                    h1 = False
                    break
            if h1:
                for s1 in S:
                    for s2 in S:
                        prod = s1 * s2
                        if not any(is_equal(prod, s) for s in S):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        if hasattr(witness, 'h2'):
            h2 = bool(witness.h2())
        elif hasattr(witness, 'n_is_positive_integer'):
            h2 = bool(witness.n_is_positive_integer())
        elif n is not None:
            h2 = int(n) == n and n > 0
    except Exception:
        h2 = False

    # neg_Q: S^{-1}(M_n(R)) is not isomorphic to M_n(S^{-1}R)
    # This fails when S does not satisfy the Ore condition, meaning the localization does not exist.
    try:
        if hasattr(witness, 'neg_q'):
            neg_q = bool(witness.neg_q())
        elif hasattr(witness, 'conclusion_fails'):
            neg_q = bool(witness.conclusion_fails())
        elif R is not None and S is not None:
            try:
                if len(R) * len(S) > 1000:
                    raise ValueError("Too large for exhaustive search")
            except Exception:
                raise ValueError("Cannot determine size")

            left_ore = True
            for r in R:
                for s in S:
                    found = False
                    for r_prime in R:
                        for s_prime in S:
                            if is_equal(s_prime * r, r_prime * s):
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        left_ore = False
                        break
                if not left_ore:
                    break
            
            right_ore = True
            for r in R:
                for s in S:
                    found = False
                    for r_prime in R:
                        for s_prime in S:
                            if is_equal(r * s_prime, s * r_prime):
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        right_ore = False
                        break
                if not right_ore:
                    break

            neg_q = not (left_ore and right_ore)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: n is a positive integer",
    "¬Q: S^{-1}(M_n(R)) is not isomorphic to M_n(S^{-1}R)"
]

N_HYP = 2
NEG_Q_INDEX = 2