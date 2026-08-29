import sympy
from sympy.matrices import eye, zeros
import itertools
import functools
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    witness is expected to be a tuple: (R, add, mul, zero, Q)
    where:
      - R is a list of elements in the ring.
      - add is a callable add(a, b) for ring addition.
      - mul is a callable mul(a, b) for ring multiplication.
      - zero is the additive identity element.
      - Q is a list of elements representing the ideal Q.
    """
    try:
        R, add, mul, zero, Q = witness
    except Exception:
        return [False, False, False]

    # Check if R is a valid ring
    try:
        is_ring = True
        if zero not in R:
            is_ring = False
        else:
            for a in R:
                if add(a, zero) != a or add(zero, a) != a:
                    is_ring = False
                    break
                has_inv = False
                for b in R:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    is_ring = False
                    break
                for b in R:
                    if add(a, b) not in R or mul(a, b) not in R:
                        is_ring = False
                        break
                    if add(a, b) != add(b, a):
                        is_ring = False
                        break
                    for c in R:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            is_ring = False
                            break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)):
                            is_ring = False
                            break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            is_ring = False
                            break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                            is_ring = False
                            break
                    if not is_ring:
                        break
                if not is_ring:
                    break
    except Exception:
        is_ring = False

    # Helper to check if a subset is an ideal
    def is_ideal(S):
        if not S: return False
        if zero not in S: return False
        for a in S:
            for b in S:
                if add(a, b) not in S: return False
        for a in S:
            for r in R:
                if mul(r, a) not in S: return False
                if mul(a, r) not in S: return False
        return True

    # H1: Q is a proper ideal of R
    try:
        h1 = is_ring and is_ideal(Q) and len(Q) < len(R)
    except Exception:
        h1 = False

    # Compute rad(Q) = {a in R | a^n in Q for some n > 0}
    try:
        rad_Q = []
        for a in R:
            curr = a
            for n in range(1, len(R) + 1):
                if curr in Q:
                    rad_Q.append(a)
                    break
                curr = mul(curr, a)
    except Exception:
        rad_Q = []

    # Find all ideals of R
    try:
        principal_ideals = []
        for a in R:
            gen = [a]
            while True:
                new_elements = list(gen)
                def add_if_new(val):
                    if val not in new_elements:
                        new_elements.append(val)
                for u in gen:
                    for v in gen:
                        add_if_new(add(u, v))
                for u in gen:
                    for r in R:
                        add_if_new(mul(r, u))
                        add_if_new(mul(u, r))
                if len(new_elements) == len(gen):
                    break
                gen = new_elements
            principal_ideals.append(sorted(gen, key=lambda e: R.index(e) if e in R else id(e)))
            
        unique_pi = []
        for pi in principal_ideals:
            if pi not in unique_pi:
                unique_pi.append(pi)
                
        ideals = [ [zero] ]
        for pi in unique_pi:
            new_ideals = []
            for I in ideals:
                sum_ideal = []
                for u in I:
                    for v in pi:
                        val = add(u, v)
                        if val not in sum_ideal:
                            sum_ideal.append(val)
                sum_ideal_list = sorted(sum_ideal, key=lambda e: R.index(e) if e in R else id(e))
                if sum_ideal_list not in ideals and sum_ideal_list not in new_ideals:
                    new_ideals.append(sum_ideal_list)
            ideals.extend(new_ideals)
    except Exception:
        ideals = []

    # H2: For any two ideals I and J of R, if I J \subseteq Q and I \not\subseteq Q, then J \subseteq \sqrt{Q}
    try:
        h2 = True
        for I in ideals:
            for J in ideals:
                IJ_gens = []
                for u in I:
                    for v in J:
                        val = mul(u, v)
                        if val not in IJ_gens:
                            IJ_gens.append(val)
                
                IJ = list(IJ_gens)
                while True:
                    new_IJ = list(IJ)
                    def add_if_new_IJ(val):
                        if val not in new_IJ:
                            new_IJ.append(val)
                    for u in IJ:
                        for v in IJ:
                            add_if_new_IJ(add(u, v))
                    if len(new_IJ) == len(IJ):
                        break
                    IJ = new_IJ
                
                IJ_sub_Q = all(u in Q for u in IJ)
                I_not_sub_Q = any(u not in Q for u in I)
                
                if IJ_sub_Q and I_not_sub_Q:
                    J_sub_rad_Q = all(u in rad_Q for u in J)
                    if not J_sub_rad_Q:
                        h2 = False
                        break
            if not h2:
                break
    except Exception:
        h2 = False

    # Negated Conclusion: Q is NOT a primary ideal.
    # (i.e., there exist x, y in R such that xy in Q, x not in Q, but y not in rad(Q))
    try:
        is_primary = True
        for u in R:
            for v in R:
                if mul(u, v) in Q and u not in Q:
                    if v not in rad_Q:
                        is_primary = False
                        break
            if not is_primary:
                break
        neg_q = not is_primary
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is a proper ideal of R",
    "H_2: For any ideals I, J, if IJ <= Q and I not <= Q, then J <= rad(Q)",
    "¬Q: Q is not a primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2