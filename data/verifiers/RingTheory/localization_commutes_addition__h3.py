import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# For this domain, we evaluate the conjecture in finite rings Z/NZ.
# The witness is expected to be a 4-tuple: (N, S, I, J)
# where N is an integer >= 2 (representing the ring R = Z/NZ),
# S is a list/set of integers for the multiplicatively closed subset,
# and I, J are lists/sets of integers representing the subsets.

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}(I + J) != S^{-1}I + S^{-1}J as ideals in S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        N, S, I, J = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    # We use R = Z/NZ, so we just need N >= 2. We cap N at 200 to ensure fast execution.
    try:
        h1 = isinstance(N, int) and 2 <= N <= 200
    except Exception:
        h1 = False
        
    # H_2: S is a multiplicatively closed subset of R
    try:
        S_set = set(s % N for s in S)
        if not S_set or 1 not in S_set:
            h2 = False
        else:
            h2 = all((s1 * s2) % N in S_set for s1 in S_set for s2 in S_set)
    except Exception:
        h2 = False
        
    # ¬Q: S^{-1}(I + J) != S^{-1}I + S^{-1}J as ideals in S^{-1}R
    try:
        S_tuple = tuple(sorted(set(s % N for s in S)))
        I_tuple = tuple(sorted(set(i % N for i in I)))
        J_tuple = tuple(sorted(set(j % N for j in J)))
        
        if not S_tuple:
            neg_Q = False
        else:
            # Precompute zero divisors of S to speed up equivalence class computation
            zero_divisors_of_S = set()
            for val in range(N):
                for u in S_tuple:
                    if (u * val) % N == 0:
                        zero_divisors_of_S.add(val)
                        break
                        
            class_cache = {}
            def get_class(a, s):
                if (a, s) in class_cache:
                    return class_cache[(a, s)]
                cls = []
                for b in range(N):
                    for t in S_tuple:
                        # (a, s) ~ (b, t) iff there exists u in S such that u*(a*t - b*s) == 0 mod N
                        if (a * t - b * s) % N in zero_divisors_of_S:
                            cls.append((b, t))
                res = tuple(sorted(cls))
                class_cache[(a, s)] = res
                return res
                
            # Compute S^{-1}(I + J)
            lhs_classes = set()
            for i in I_tuple:
                for j in J_tuple:
                    x_val = (i + j) % N
                    for s in S_tuple:
                        lhs_classes.add(get_class(x_val, s))
                        
            # Compute S^{-1}I + S^{-1}J
            rhs_classes = set()
            for i in I_tuple:
                for s1 in S_tuple:
                    for j in J_tuple:
                        for s2 in S_tuple:
                            num = (i * s2 + j * s1) % N
                            den = (s1 * s2) % N
                            rhs_classes.add(get_class(num, den))
                            
            # The conclusion fails if the resulting subsets in S^{-1}R are not equal
            neg_Q = (lhs_classes != rhs_classes)
    except Exception:
        neg_Q = False
        
    return [h1, h2, neg_Q]