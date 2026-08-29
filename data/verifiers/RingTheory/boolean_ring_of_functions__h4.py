import itertools
import sympy

# Top-level setup
# (No specific named objects required for this Boolean ring verifier)

def is_boolean_ring(ring):
    try:
        if hasattr(ring, 'elements'):
            elements = list(ring.elements)
        else:
            return False
            
        elem_set = set(elements)
        zero = ring.zero
        
        if zero not in elem_set:
            return False
            
        # Check closure and boolean property
        for x in elements:
            xx = ring.mul(x, x)
            if xx not in elem_set: return False
            if xx != x: return False
                
        # Ring axioms
        for a in elements:
            # Identity for addition
            if ring.add(a, zero) != a: return False
            if ring.add(zero, a) != a: return False
            
            # Additive inverse
            has_inv = False
            for b in elements:
                ab = ring.add(a, b)
                if ab not in elem_set: return False
                if ab == zero and ring.add(b, a) == zero:
                    has_inv = True
            if not has_inv: return False
            
            # Commutativity of addition
            for b in elements:
                ab = ring.add(a, b)
                ba = ring.add(b, a)
                if ab != ba: return False
                
                mab = ring.mul(a, b)
                if mab not in elem_set: return False
                
                # Associativity and Distributivity
                for c in elements:
                    if ring.add(ab, c) != ring.add(a, ring.add(b, c)): return False
                    if ring.mul(mab, c) != ring.mul(a, ring.mul(b, c)): return False
                    if ring.mul(a, ring.add(b, c)) != ring.add(mab, ring.mul(a, c)): return False
                    if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)): return False
                    
        return True
    except Exception:
        return False

def conditions(witness):
    # H1: X is a non-empty set
    try:
        X = list(witness.X)
        h1 = len(X) > 0
    except Exception:
        h1 = False

    # H2: R is a Boolean ring
    try:
        R = witness.R
        h2 = is_boolean_ring(R)
    except Exception:
        h2 = False

    # H3: R^X is the set of all functions from X to R
    try:
        X = list(witness.X)
        R = witness.R
        R_X = witness.R_X
        
        expected_elements = set(itertools.product(R.elements, repeat=len(X)))
        
        if hasattr(R_X, 'elements'):
            actual_elements = list(R_X.elements)
        else:
            actual_elements = list(R_X)
            
        parsed_elements = []
        for e in actual_elements:
            if isinstance(e, dict):
                parsed_elements.append(tuple(e[x] for x in X))
            elif isinstance(e, list):
                parsed_elements.append(tuple(e))
            else:
                parsed_elements.append(e)
                
        actual_set = set(parsed_elements)
        h3 = (expected_elements == actual_set)
    except Exception:
        h3 = False

    # neg_Q: R^X is NOT a Boolean ring
    try:
        R_X = witness.R_X
        neg_q = not is_boolean_ring(R_X)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: R is a Boolean ring",
    "H_3: R^X is the set of all functions from X to R",
    "¬Q: R^X is not a Boolean ring"
]

N_HYP = 3
NEG_Q_INDEX = 3