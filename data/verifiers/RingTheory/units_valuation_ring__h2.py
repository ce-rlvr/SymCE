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
# (No specific named objects required for this RingTheory theorem)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            v = witness.get('v')
            R = witness.get('R')
            u = witness.get('u')
            add = witness.get('add', lambda x, y: x + y)
            mul = witness.get('mul', lambda x, y: x * y)
        elif isinstance(witness, tuple) and len(witness) == 4:
            K, v, R, u = witness
            add = lambda x, y: x + y
            mul = lambda x, y: x * y
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # Extract elements of K
    try:
        if isinstance(K, (list, tuple, set)):
            K_elements = list(K)
        else:
            K_elements = list(K)
    except Exception:
        K_elements = None

    # We require a finite field for verification by iteration
    if K_elements is None or len(K_elements) > 50:
        return [False, False, False, False]

    # Ensure unique elements in K
    try:
        unique_K = []
        for x in K_elements:
            if x not in unique_K:
                unique_K.append(x)
        K_elements = unique_K
    except Exception:
        pass

    # Find additive and multiplicative identities
    try:
        zero = None
        for e in K_elements:
            if all(add(x, e) == x for x in K_elements) and all(add(e, x) == x for x in K_elements):
                zero = e
                break
        
        one = None
        for e in K_elements:
            if all(mul(x, e) == x for x in K_elements) and all(mul(e, x) == x for x in K_elements):
                one = e
                break
    except Exception:
        zero = None
        one = None

    # H_1: K is a field
    try:
        h1 = False
        if zero is not None and one is not None and zero != one:
            h1 = True
            for a in K_elements:
                # Additive inverse
                if not any(add(a, b) == zero for b in K_elements):
                    h1 = False; break
                # Multiplicative inverse for non-zero elements
                if a != zero:
                    if not any(mul(a, b) == one for b in K_elements):
                        h1 = False; break
                # Closure, commutativity, associativity, distributivity
                for b in K_elements:
                    if add(a, b) not in K_elements: h1 = False; break
                    if mul(a, b) not in K_elements: h1 = False; break
                    if add(a, b) != add(b, a): h1 = False; break
                    if mul(a, b) != mul(b, a): h1 = False; break
                    for c in K_elements:
                        if add(add(a, b), c) != add(a, add(b, c)): h1 = False; break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False; break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False; break
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    # H_2: R = {x \in K^{\times} \mid v(x) \geq 0} \cup {0}
    try:
        expected_R = []
        for x in K_elements:
            if x == zero:
                expected_R.append(x)
            else:
                if bool(v(x) >= 0):
                    expected_R.append(x)
        
        R_elements = list(R)
        unique_R = []
        for x in R_elements:
            if x not in unique_R:
                unique_R.append(x)
        R_elements = unique_R

        h2 = True
        if len(R_elements) != len(expected_R):
            h2 = False
        else:
            for x in R_elements:
                if x not in expected_R:
                    h2 = False
                    break
            for x in expected_R:
                if x not in R_elements:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: u is a non-zero element of R
    try:
        h3 = (u in R_elements) and (u != zero)
    except Exception:
        h3 = False

    # ¬Q: u is a unit in R if and only if v(u) = 0 (Conclusion fails)
    try:
        # Check if u is a unit in R
        is_unit = False
        for w in R_elements:
            if mul(u, w) == one:
                is_unit = True
                break
        
        v_is_zero = bool(v(u) == 0)
        
        # The conclusion is (is_unit == v_is_zero). We want it to fail.
        neg_q = (is_unit != v_is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: R = {x in K^x | v(x) >= 0} U {0} is the valuation ring associated with v",
    "H_3: u is a non-zero element of R",
    "¬Q: u is a unit in R is not equivalent to v(u) = 0"
]

N_HYP = 3
NEG_Q_INDEX = 3