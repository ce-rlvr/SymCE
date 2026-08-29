import sympy
from sympy import Symbol, QQ, ZZ, RR, CC

# Top-level setup for potential witness expressions
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

QQ_x = QQ.old_poly_ring(x)
ZZ_x = ZZ.old_poly_ring(x)
RR_x = RR.old_poly_ring(x)
CC_x = CC.old_poly_ring(x)

QQ_xy = QQ.old_poly_ring(x, y)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let k be a field, Let A be a k-algebra. Then A is an Artinian ring."
    """
    # Extract k and A from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            k, A = witness
        else:
            A = witness
            # Infer k from A's domain hierarchy if not explicitly provided
            curr = A
            seen = set()
            while hasattr(curr, 'domain') and curr != curr.domain:
                if curr in seen:
                    break
                seen.add(curr)
                curr = curr.domain
            k = curr
    except Exception:
        return [False, False, False]

    # H_1: k is a field
    try:
        h1 = bool(getattr(k, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: A is a k-algebra
    try:
        h2 = False
        if getattr(A, 'is_Ring', False):
            curr = A
            seen = set()
            while hasattr(curr, 'domain') and curr != curr.domain:
                if curr == k:
                    h2 = True
                    break
                if curr in seen:
                    break
                seen.add(curr)
                curr = curr.domain
            if curr == k:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: A is not an Artinian ring
    # In SymPy, domains are integral domains. An Artinian integral domain is necessarily a field.
    try:
        if hasattr(A, 'ideal') and hasattr(A, 'base_ring'):
            # If A is a quotient ring, we assume it is Artinian unless its ideal is zero.
            # (Finite-dimensional algebras over a field are Artinian).
            try:
                zero_ideal = False
                if hasattr(A.ideal, 'is_zero'):
                    if callable(A.ideal.is_zero):
                        zero_ideal = A.ideal.is_zero()
                    else:
                        zero_ideal = A.ideal.is_zero
                
                if zero_ideal:
                    is_artinian = False
                else:
                    is_artinian = True
            except Exception:
                is_artinian = True
        else:
            is_artinian = bool(getattr(A, 'is_Field', False))
            
        neg_q = not is_artinian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: A is a k-algebra",
    "¬Q: A is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2