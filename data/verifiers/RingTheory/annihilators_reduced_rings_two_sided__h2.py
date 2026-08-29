import sympy
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        try:
            eq = (a == b)
            return bool(eq.all())
        except Exception:
            return False

def contains(lst, item):
    return any(is_eq(e, item) for e in lst)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            R, x_elem, L = witness
        elif len(witness) == 2:
            R, x_elem = witness
            R_list = list(R)
            zero = R_list[0] - R_list[0]
            L = [a for a in R_list if is_eq(a * x_elem, zero)]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a reduced ring
    h1 = False
    try:
        if hasattr(R, 'is_reduced_ring') and callable(R.is_reduced_ring):
            h1 = bool(R.is_reduced_ring())
        else:
            R_list = list(R)
            if 0 < len(R_list) <= 2000:
                zero = R_list[0] - R_list[0]
                is_ring = True
                
                use_set = False
                if R_list:
                    first = R_list[0]
                    if isinstance(first, (int, sympy.Integer, str, tuple)):
                        use_set = True
                
                if use_set:
                    try:
                        R_set = set(R_list)
                        def in_R(item): return item in R_set
                    except TypeError:
                        def in_R(item): return contains(R_list, item)
                else:
                    def in_R(item): return contains(R_list, item)
                
                # Check closure
                for a in R_list:
                    for b in R_list:
                        if not in_R(a + b): is_ring = False; break
                        if not in_R(a * b): is_ring = False; break
                    if not is_ring: break
                
                # Check additive group axioms
                if is_ring:
                    for a in R_list:
                        if not is_eq(a + zero, a): is_ring = False; break
                        if not is_eq(zero + a, a): is_ring = False; break
                        if not in_R(zero - a): is_ring = False; break
                        if not is_eq(a + (zero - a), zero): is_ring = False; break
                        
                # Check associativity and distributivity (optimized for large rings)
                if is_ring:
                    subset_a = R_list if len(R_list) <= 50 else R_list[:15]
                    subset_b = R_list if len(R_list) <= 50 else R_list[:15]
                    for a in subset_a:
                        for b in subset_b:
                            for c in R_list:
                                if not is_eq((a + b) + c, a + (b + c)): is_ring = False; break
                                if not is_eq((a * b) * c, a * (b * c)): is_ring = False; break
                                if not is_eq(a * (b + c), a * b + a * c): is_ring = False; break
                                if not is_eq((a + b) * c, a * c + b * c): is_ring = False; break
                            if not is_ring: break
                        if not is_ring: break
                        
                # Check reduced property (no non-zero nilpotent elements)
                if is_ring:
                    is_reduced = True
                    for a in R_list:
                        if not is_eq(a, zero):
                            p = a
                            is_nil = False
                            for _ in range(len(R_list)):
                                if is_eq(p, zero):
                                    is_nil = True
                                    break
                                p = p * a
                            if is_nil:
                                is_reduced = False
                                break
                    h1 = is_reduced
    except Exception:
        h1 = False

    # H2: L is the left annihilator of x
    h2 = False
    try:
        R_list = list(R)
        zero = R_list[0] - R_list[0]
        expected_L = [a for a in R_list if is_eq(a * x_elem, zero)]
        if len(L) == len(expected_L):
            h2 = all(contains(expected_L, a) for a in L)
    except Exception:
        h2 = False

    # neg_Q: L is not a two-sided ideal of R
    neg_q = False
    try:
        R_list = list(R)
        L_list = list(L)
        zero = R_list[0] - R_list[0]
        
        if not L_list:
            is_ideal = False
        else:
            use_set = False
            if L_list:
                first = L_list[0]
                if isinstance(first, (int, sympy.Integer, str, tuple)):
                    use_set = True
            
            if use_set:
                try:
                    L_set = set(L_list)
                    def in_L(item): return item in L_set
                except TypeError:
                    def in_L(item): return contains(L_list, item)
            else:
                def in_L(item): return contains(L_list, item)

            is_ideal = True
            
            # Check if L is an additive subgroup
            for a in L_list:
                for b in L_list:
                    if not in_L(a + b): is_ideal = False; break
                if not in_L(zero - a): is_ideal = False; break
                if not is_ideal: break
                
            # Check left and right ideal properties
            if is_ideal:
                for r in R_list:
                    for a in L_list:
                        if not in_L(r * a): is_ideal = False; break
                        if not in_L(a * r): is_ideal = False; break
                    if not is_ideal: break
                
        neg_q = not is_ideal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "H_2: L is the left annihilator of x",
    "¬Q: L is not a two-sided ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2