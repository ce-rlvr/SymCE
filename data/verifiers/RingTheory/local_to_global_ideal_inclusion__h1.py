import itertools
import sympy

class RingWitness:
    """
    A witness representing a finite ring and two ideals.
    elements: list of elements
    add: callable add(a, b)
    mul: callable mul(a, b)
    zero: the zero element
    I: list of elements in ideal I
    J: list of elements in ideal J
    """
    def __init__(self, elements, add_func, mul_func, zero, I, J):
        self.elements = elements
        self.add = add_func
        self.mul = mul_func
        self.zero = zero
        self.I = I
        self.J = J

def conditions(witness) -> list[bool]:
    try:
        elements = witness.elements
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        I = witness.I
        J = witness.J
        
        n = len(elements)
        if n > 10 or n < 1:
            return [False, False, False]
            
        def check_is_ring():
            if zero not in elements: return False
            for a in elements:
                if add(a, zero) != a: return False
                has_inv = False
                for b in elements:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv: return False
                for b in elements:
                    if add(a, b) != add(b, a): return False
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            return True
            
        if not check_is_ring():
            return [False, False, False]
            
        def is_ideal(subset):
            if not subset: return False
            if not set(subset).issubset(set(elements)): return False
            if zero not in subset: return False
            for a in subset:
                for b in subset:
                    if add(a, b) not in subset: return False
            for r in elements:
                for x in subset:
                    if mul(r, x) not in subset: return False
                    if mul(x, r) not in subset: return False
            return True

        try:
            h1 = is_ideal(I)
        except Exception:
            h1 = False
            
        try:
            h2 = is_ideal(J)
        except Exception:
            h2 = False
            
        try:
            ideals = []
            for r_size in range(1, n + 1):
                for subset in itertools.combinations(elements, r_size):
                    if is_ideal(subset):
                        ideals.append(list(subset))
                        
            proper_ideals = [idl for idl in ideals if len(idl) < n]
            maximal_ideals = []
            for idl in proper_ideals:
                is_max = True
                for other in proper_ideals:
                    if idl != other and set(idl).issubset(set(other)):
                        is_max = False
                        break
                if is_max:
                    maximal_ideals.append(idl)
                    
            i_subset_j = set(I).issubset(set(J))
            
            local_inclusion = True
            for M in maximal_ideals:
                R_minus_M = [r for r in elements if r not in M]
                for x in I:
                    found = False
                    for s in R_minus_M:
                        if mul(s, x) in J:
                            found = True
                            break
                    if not found:
                        local_inclusion = False
                        break
                if not local_inclusion:
                    break
                    
            neg_q = (not i_subset_j) and local_inclusion
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: I is not a subset of J, but I_M is a subset of J_M for every maximal ideal M"
]

N_HYP = 2
NEG_Q_INDEX = 2