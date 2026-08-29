import sympy as sp

# Top-level setup
# Define phi so that it can be used in witness expressions
phi = (1 + sp.sqrt(5)) / 2

def conditions(witness):
    h1 = False
    neg_q = False
    
    def parse_element(w):
        # Check if w is provided as a tuple/list of two integers (u, v) representing u + v*phi
        if isinstance(w, (tuple, list)) and len(w) == 2:
            try:
                u = int(w[0])
                v = int(w[1])
                if u == w[0] and v == w[1]:
                    return u, v
            except Exception:
                pass
        
        # Check if w is provided as a SymPy expression
        try:
            expr = sp.expand(sp.sympify(w))
            a, terms = expr.as_coeff_add()
            b_term = sum(terms)
            b = sp.simplify(b_term / sp.sqrt(5))
            if b.is_rational and a.is_rational:
                v = 2 * b
                u = a - b
                if u.is_integer and v.is_integer:
                    return int(u), int(v)
        except Exception:
            pass
        
        return None

    try:
        # Case 1: The witness is a single element of R
        parsed = parse_element(witness)
        if parsed is not None:
            h1 = True
            u, v = parsed
            # The algebraic norm N(u + v*phi) = u^2 + u*v - v^2
            norm = u**2 + u*v - v**2
            # A Euclidean function must map to non-negative integers.
            # If the norm is negative, N is not a valid Euclidean function.
            neg_q = norm < 0
            return [h1, neg_q]
            
        # Case 2: The witness is a pair of elements in R
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            p1 = parse_element(witness[0])
            p2 = parse_element(witness[1])
            if p1 is not None and p2 is not None:
                h1 = True
                u1, v1 = p1
                u2, v2 = p2
                norm1 = u1**2 + u1*v1 - v1**2
                norm2 = u2**2 + u2*v2 - v2**2
                # If either element has a negative norm, N is not a valid Euclidean function.
                neg_q = norm1 < 0 or norm2 < 0
                return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is an element (or pair of elements) in R",
    "¬Q: N takes a negative value at the witness, so N is not a valid Euclidean function"
]

N_HYP = 1
NEG_Q_INDEX = 1