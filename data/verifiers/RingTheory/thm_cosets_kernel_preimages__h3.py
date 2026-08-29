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
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    The witness should be a dictionary containing:
      'R': a set or list of elements in the domain ring
      'S': a set or list of elements in the codomain ring
      'add_R': a function (x, y) -> x + y in R
      'mul_R': a function (x, y) -> x * y in R
      'add_S': a function (x, y) -> x + y in S
      'mul_S': a function (x, y) -> x * y in S
      'zero_R': the additive identity of R
      'zero_S': the additive identity of S
      'f': a function x -> f(x) from R to S
      'K': a set or list of elements in R representing the kernel of f
      'r': an element in R
      's': an element in S
    """
    # H_1: R and S are rings
    try:
        R = witness['R']
        S = witness['S']
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_R = witness['zero_R']
        zero_S = witness['zero_S']
        
        def is_ring(elements, add, mul, zero):
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    return False
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    return False
                for b in elements:
                    if add(a, b) not in elements: return False
                    if mul(a, b) not in elements: return False
                    if add(a, b) != add(b, a): return False
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            return True

        h1_ok = is_ring(R, add_R, mul_R, zero_R) and is_ring(S, add_S, mul_S, zero_S)
    except Exception:
        h1_ok = False

    # H_2: f: R -> S is a ring homomorphism with kernel K
    try:
        f = witness['f']
        K = witness['K']
        
        is_hom = True
        for a in R:
            if f(a) not in S:
                is_hom = False
                break
            for b in R:
                if f(add_R(a, b)) != add_S(f(a), f(b)):
                    is_hom = False
                    break
                if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                    is_hom = False
                    break
        
        actual_K = [x for x in R if f(x) == zero_S]
        
        # Check if K and actual_K contain the same elements
        is_kernel = True
        for k in K:
            if k not in actual_K:
                is_kernel = False
                break
        for k in actual_K:
            if k not in K:
                is_kernel = False
                break
                
        h2_ok = is_hom and is_kernel
    except Exception:
        h2_ok = False

    # H_3: r in R is an element such that f(r) = s
    try:
        r = witness['r']
        s = witness['s']
        h3_ok = (r in R) and (s in S) and (f(r) == s)
    except Exception:
        h3_ok = False

    # ¬Q: The preimage f^(-1)({s}) is NOT exactly the coset r + K
    try:
        preimage = [x for x in R if f(x) == s]
        coset = [add_R(r, k) for k in K]
        
        # Check if they are exactly the same sets
        same_sets = True
        for p in preimage:
            if p not in coset:
                same_sets = False
                break
        for c in coset:
            if c not in preimage:
                same_sets = False
                break
        
        neg_q_ok = not same_sets
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism with kernel K",
    "H_3: r in R is an element such that f(r) = s",
    "¬Q: The preimage f^(-1)({s}) is not exactly the coset r + K"
]

N_HYP = 3
NEG_Q_INDEX = 3