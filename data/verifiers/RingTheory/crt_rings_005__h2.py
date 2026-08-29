import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import math
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be provided as either:
      (R, I_list, x_list)  - assuming elements support + and * directly
      (R, add, mul, I_list, x_list) - providing custom addition and multiplication functions
    """
    try:
        if len(witness) == 3:
            R, I_list, x_list = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
        elif len(witness) == 5:
            R, add, mul, I_list, x_list = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring with identity
    try:
        h1 = False
        if isinstance(R, list) and len(R) > 0 and len(R) <= 64:
            # Find additive identity (zero)
            zero = None
            for e in R:
                if all(add(e, elem) == elem and add(elem, e) == elem for elem in R):
                    zero = e
                    break
            
            if zero is not None:
                valid_ring = True
                # Check additive inverses and closure
                for elem in R:
                    has_inv = False
                    for inv in R:
                        if add(elem, inv) == zero and add(inv, elem) == zero:
                            has_inv = True
                            break
                    if not has_inv:
                        valid_ring = False
                        break
                    for elem2 in R:
                        if add(elem, elem2) not in R:
                            valid_ring = False
                            break
                        if mul(elem, elem2) not in R:
                            valid_ring = False
                            break
                    if not valid_ring:
                        break
                
                if valid_ring:
                    # Find multiplicative identity (one)
                    one = None
                    for e in R:
                        if all(mul(e, elem) == elem and mul(elem, e) == elem for elem in R):
                            one = e
                            break
                    
                    if one is not None:
                        # Check associativity and distributivity
                        for a in R:
                            if not valid_ring: break
                            for b in R:
                                if not valid_ring: break
                                if add(a, b) != add(b, a):
                                    valid_ring = False
                                    break
                                for c in R:
                                    if add(add(a, b), c) != add(a, add(b, c)):
                                        valid_ring = False
                                    elif mul(mul(a, b), c) != mul(a, mul(b, c)):
                                        valid_ring = False
                                    elif mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                                        valid_ring = False
                                    elif mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                                        valid_ring = False
                                    if not valid_ring:
                                        break
                        h1 = valid_ring
    except Exception:
        h1 = False

    # H2: I_i + I_j = R for all i != j
    try:
        h2 = False
        if isinstance(I_list, list) and len(I_list) >= 2:
            subsets_ok = True
            for I in I_list:
                for a in I:
                    if a not in R:
                        subsets_ok = False
                        break
            if subsets_ok:
                coprime_ok = True
                n = len(I_list)
                for i in range(n):
                    for j in range(i + 1, n):
                        sums = []
                        for a in I_list[i]:
                            for b in I_list[j]:
                                sums.append(add(a, b))
                        for r in R:
                            if r not in sums:
                                coprime_ok = False
                                break
                        if not coprime_ok:
                            break
                    if not coprime_ok:
                        break
                h2 = coprime_ok
    except Exception:
        h2 = False

    # H3: x_1, ..., x_n are elements of R
    try:
        h3 = False
        if isinstance(x_list, list) and len(x_list) == len(I_list):
            h3 = all(x in R for x in x_list)
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails (There is NO element x in R such that x = x_k mod I_k for all k)
    try:
        neg_q = False
        if isinstance(I_list, list) and isinstance(x_list, list) and len(I_list) == len(x_list):
            zero = None
            for e in R:
                if all(add(e, elem) == elem and add(elem, e) == elem for elem in R):
                    zero = e
                    break
            
            if zero is not None:
                exists_x = False
                for test_x in R:
                    valid_for_all_k = True
                    for k in range(len(I_list)):
                        xk = x_list[k]
                        inv_xk = None
                        for a in R:
                            if add(xk, a) == zero and add(a, xk) == zero:
                                inv_xk = a
                                break
                        
                        if inv_xk is None:
                            valid_for_all_k = False
                            break
                        
                        # x = x_k mod I_k  <=>  x - x_k in I_k
                        diff = add(test_x, inv_xk)
                        if diff not in I_list[k]:
                            valid_for_all_k = False
                            break
                            
                    if valid_for_all_k:
                        exists_x = True
                        break
                
                neg_q = not exists_x
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I_i + I_j = R for all i != j",
    "H_3: x_1, ..., x_n are elements of R",
    "¬Q: There is no element x in R such that x ≡ x_k (mod I_k) for all k"
]

N_HYP = 3
NEG_Q_INDEX = 3