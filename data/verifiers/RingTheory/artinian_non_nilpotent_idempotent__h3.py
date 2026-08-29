import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is a right Artinian ring
    # We verify that R is a finite ring (all finite rings are right Artinian).
    h1 = False
    elements = []
    add = None
    mult = None
    eq = None
    zero = None

    try:
        if isinstance(R, int):
            if R > 1:
                elements = list(range(R))
                def add(a, b): return (a + b) % R
                def mult(a, b): return (a * b) % R
                def eq(a, b): return (a % R) == (b % R)
                zero = 0
                h1 = True
        elif isinstance(R, list) and len(R) > 0:
            elements = R
            def add(a, b): return a + b
            def mult(a, b): return a * b
            def eq(a, b): return a == b
            
            closed = True
            for a in elements:
                for b in elements:
                    s = add(a, b)
                    if not any(eq(s, e) for e in elements):
                        closed = False
                        break
                    p = mult(a, b)
                    if not any(eq(p, e) for e in elements):
                        closed = False
                        break
                if not closed:
                    break
            
            if closed:
                for e in elements:
                    if all(eq(add(e, _x), _x) and eq(add(_x, e), _x) for _x in elements):
                        zero = e
                        break
                if zero is not None:
                    is_ring = True
                    for a in elements:
                        if not any(eq(add(a, b), zero) for b in elements):
                            is_ring = False
                            break
                    h1 = is_ring
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]

    # H2: I is a right ideal of R
    h2 = False
    try:
        if isinstance(I, list) and len(I) > 0:
            is_subset = True
            for i in I:
                if not any(eq(i, e) for e in elements):
                    is_subset = False
                    break
            
            if is_subset:
                closed_add = True
                for a in I:
                    for b in I:
                        s = add(a, b)
                        if not any(eq(s, i) for i in I):
                            closed_add = False
                            break
                    if not closed_add:
                        break
                
                closed_mult = True
                for a in I:
                    for r in elements:
                        p = mult(a, r)
                        if not any(eq(p, i) for i in I):
                            closed_mult = False
                            break
                    if not closed_mult:
                        break
                
                has_zero = any(eq(i, zero) for i in I)
                
                if closed_add and closed_mult and has_zero:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: I does NOT contain a non-zero idempotent element
    neg_q = False
    try:
        if h2:
            has_nonzero_idempotent = False
            for i in I:
                if not eq(i, zero):
                    if eq(mult(i, i), i):
                        has_nonzero_idempotent = True
                        break
            neg_q = not has_nonzero_idempotent
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: I is a right ideal of R",
    "¬Q: I contains no non-zero idempotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2