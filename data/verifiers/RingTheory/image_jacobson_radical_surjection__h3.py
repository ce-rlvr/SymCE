import itertools
from sympy import Rational, Integer
from sympy.abc import x, y, z

def is_ring(R):
    try:
        elements = list(R.elements)
        zero = R.zero
        if zero not in elements: 
            return False
        
        # Check identity properties
        for a in elements:
            if R.add(a, zero) != a: return False
            if R.add(zero, a) != a: return False
            if R.mul(a, zero) != zero: return False
            if R.mul(zero, a) != zero: return False
            
        # Deterministic check for associativity and distributivity
        triples = list(itertools.product(elements, repeat=3))
        if len(triples) > 2000:
            triples = triples[:2000]
        for a, b, c in triples:
            if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
            if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
            if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
            if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
            
        pairs = list(itertools.product(elements, repeat=2))
        if len(pairs) > 2000:
            pairs = pairs[:2000]
        for a, b in pairs:
            if R.add(a, b) not in elements: return False
            if R.mul(a, b) not in elements: return False
            if R.add(a, b) != R.add(b, a): return False
            
        # Check additive inverses
        for a in elements:
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        return True
    except Exception:
        return False

def is_surjective_homomorphism(R, S, f):
    try:
        def apply_f(val):
            if isinstance(f, dict):
                return f[val]
            return f(val)
            
        mapped_elements = set()
        for a in R.elements:
            fa = apply_f(a)
            if fa not in S.elements:
                return False
            mapped_elements.add(fa)
            
        if mapped_elements != set(S.elements):
            return False
            
        pairs = list(itertools.product(R.elements, repeat=2))
        if len(pairs) > 2000:
            pairs = pairs[:2000]
        for a, b in pairs:
            if apply_f(R.add(a, b)) != S.add(apply_f(a), apply_f(b)): return False
            if apply_f(R.mul(a, b)) != S.mul(apply_f(a), apply_f(b)): return False
            
        return True
    except Exception:
        return False

def neg_conclusion(R, S, f):
    try:
        def apply_f(val):
            if isinstance(f, dict):
                return f[val]
            return f(val)
            
        def get_J(Ring):
            # For finite rings, the Jacobson radical is the largest nilpotent ideal.
            # An element x is in J(R) iff for all y in R, xy is nilpotent.
            j_elements = []
            elements = list(Ring.elements)
            for a in elements:
                is_in_j = True
                for b in elements:
                    ab = Ring.mul(a, b)
                    curr = ab
                    seen = set()
                    is_nil = False
                    while curr not in seen:
                        if curr == Ring.zero:
                            is_nil = True
                            break
                        seen.add(curr)
                        curr = Ring.mul(curr, ab)
                    if not is_nil:
                        is_in_j = False
                        break
                if is_in_j:
                    j_elements.append(a)
            return j_elements
            
        JR = get_J(R)
        JS = get_J(S)
        
        JS_set = set(JS)
        for x_val in JR:
            fx = apply_f(x_val)
            if fx not in JS_set:
                return True # f(J(R)) is NOT contained in J(S)
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, f = witness
        else:
            R = witness.R
            S = witness.S
            f = witness.f
    except Exception:
        return [False, False, False]
        
    h1 = is_ring(R) and is_ring(S)
    h2 = is_surjective_homomorphism(R, S, f)
    neg_q = neg_conclusion(R, S, f)
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "¬Q: The image f(J(R)) is not contained in J(S)"
]

N_HYP = 2
NEG_Q_INDEX = 2