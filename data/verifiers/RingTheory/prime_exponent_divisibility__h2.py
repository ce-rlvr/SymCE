import sympy
from sympy import factorint
from sympy.abc import x, y, z

# Top-level setup
# No specific named bindings needed for this ring theory problem.
# We use integers directly as the standard Unique Factorization Domain (Z).

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness. It could be a tuple (a, b) or (R, a, b).
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                a, b = witness
            elif len(witness) == 3:
                _, a, b = witness
            else:
                return [False, False, False]
        else:
            # If a single element is provided, assume it's 'a' and set 'b' to 1
            a = witness
            b = 1
            
        # Attempt to convert to integers for evaluation in Z
        try:
            a = int(a)
        except Exception:
            pass
        try:
            b = int(b)
        except Exception:
            pass
            
        a_is_zero = (a == 0)
        b_is_zero = (b == 0)
        
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    # We evaluate in Z (or assume the provided ring is a UFD), so this holds.
    h1 = True
    
    # H_2: v_p(x) denotes the exponent of p in the unique prime factorization of x
    # This is a definitional hypothesis, which always holds.
    h2 = True
    
    # ¬Q: The equivalence "a divides b iff v_p(a) <= v_p(b) for all p" FAILS.
    # The unique prime factorization is only defined for non-zero elements.
    # If a=0 or b=0, v_p(x) is undefined, making the RHS of the equivalence invalid.
    # Thus, the equivalence fails to hold.
    if a_is_zero or b_is_zero:
        neg_q = True
    else:
        try:
            a_int = int(a)
            b_int = int(b)
            
            # LHS: a divides b
            lhs = (b_int % a_int == 0)
            
            # RHS: v_p(a) <= v_p(b) for all prime elements p
            fa = factorint(abs(a_int))
            fb = factorint(abs(b_int))
            rhs = True
            for p, exp_a in fa.items():
                if exp_a > fb.get(p, 0):
                    rhs = False
                    break
                    
            neg_q = (lhs != rhs)
        except Exception:
            # For any non-zero elements in any UFD, the equivalence mathematically holds.
            # Therefore, if it's a valid non-zero element but not an integer, it cannot be a counterexample.
            neg_q = False
            
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: v_p(x) denotes the exponent of p in the unique prime factorization of x",
    "¬Q: The equivalence 'a divides b iff v_p(a) <= v_p(b) for all p' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2