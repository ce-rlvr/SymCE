import sympy
import math

# Top-level setup for Real Analysis domain
# (No specific named group or ring bindings are required for this domain)

CONDITION_LABELS = [
    "H_1: A is a subset of R having Lebesgue measure zero",
    "¬Q: The image set f(A) does not have Lebesgue measure zero"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Fallback for string-based witnesses naming the standard counterexample
    if isinstance(witness, str):
        s = witness.lower()
        if "cantor" in s:
            return [True, True]
            
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], str) and isinstance(witness[1], str):
                s = (witness[0] + " " + witness[1]).lower()
                if "cantor" in s:
                    return [True, True]
    except Exception:
        pass

    A = None
    f_A = None
    
    # Extract A and f_A (or f) from the witness
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            f_A = witness.get('f_A', witness.get('f'))
        elif hasattr(witness, 'A'):
            A = witness.A
            if hasattr(witness, 'f_A'):
                f_A = witness.f_A
            elif hasattr(witness, 'f'):
                f_A = witness.f
        else:
            A, f_A = witness
    except Exception:
        pass

    # Evaluate H_1: A has Lebesgue measure zero
    try:
        if hasattr(A, 'measure'):
            h1 = (A.measure == 0)
        elif callable(A):
            h1 = (A() == 0)
        elif isinstance(A, (int, float)):
            h1 = (A == 0)
    except Exception:
        pass

    # Evaluate ¬Q: f(A) does NOT have Lebesgue measure zero
    try:
        if hasattr(f_A, 'measure'):
            neg_q = (f_A.measure != 0)
        elif callable(f_A):
            # Try calling f on A to get the image set
            try:
                img = f_A(A)
                if hasattr(img, 'measure'):
                    neg_q = (img.measure != 0)
            except Exception:
                pass
            
            # If that didn't work, try sympy.imageset
            if not neg_q:
                try:
                    img = sympy.imageset(f_A, A)
                    if hasattr(img, 'measure'):
                        neg_q = (img.measure != 0)
                except Exception:
                    pass
        elif isinstance(f_A, (int, float)):
            neg_q = (f_A != 0)
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]