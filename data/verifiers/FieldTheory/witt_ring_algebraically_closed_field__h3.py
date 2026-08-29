import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: K is algebraically closed",
    "¬Q: W(K) is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H1: K is a field
    h1 = False
    try:
        if isinstance(witness, str):
            w = witness.lower()
            if w in ["c", "r", "q"]: 
                h1 = True
            elif "f" in w or "k" in w or "field" in w: 
                h1 = True
        elif hasattr(witness, 'is_Field'):
            if callable(witness.is_Field):
                h1 = bool(witness.is_Field())
            else:
                h1 = bool(witness.is_Field)
        elif hasattr(witness, 'characteristic'):
            h1 = True
    except Exception:
        pass

    # H2: K is algebraically closed
    h2 = False
    try:
        if isinstance(witness, str):
            w = witness.lower()
            if w == "c": 
                h2 = True
            elif "bar" in w or "alg" in w or "closure" in w or "closed" in w: 
                h2 = True
        elif str(witness) == "CC":
            h2 = True
        elif hasattr(witness, 'is_algebraically_closed'):
            if callable(witness.is_algebraically_closed):
                h2 = bool(witness.is_algebraically_closed())
            else:
                h2 = bool(witness.is_algebraically_closed)
    except Exception:
        pass

    # neg_Q: W(K) is not isomorphic to Z/2Z
    # For an algebraically closed field K, W(K) is isomorphic to Z/2Z iff char(K) != 2.
    # If char(K) == 2, W(K) is isomorphic to Z (modulo hyperbolic spaces).
    # If K is not algebraically closed, W(K) is generally larger/different.
    neg_q = False
    try:
        char = None
        if isinstance(witness, str):
            w = witness.lower()
            if w in ["c", "r", "q"]: 
                char = 0
            else:
                if "f2" in w or "f_2" in w:
                    char = 2
                elif "f3" in w or "f_3" in w:
                    char = 3
                elif "f5" in w or "f_5" in w:
                    char = 5
                elif "char" in w:
                    if "2" in w or "two" in w:
                        char = 2
                    elif "3" in w or "three" in w:
                        char = 3
                    elif "0" in w or "zero" in w:
                        char = 0
        elif hasattr(witness, 'characteristic'):
            if callable(witness.characteristic):
                char = witness.characteristic()
            else:
                char = witness.characteristic
        
        if char == 2:
            neg_q = True
        elif not h2:
            neg_q = True
        else:
            neg_q = False
            
    except Exception:
        pass

    return [h1, h2, neg_q]