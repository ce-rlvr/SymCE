import math
import sympy

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (x, y, L) where:
      - x is a list/tuple representing a periodic sequence (x_n)
      - y is a list/tuple representing a periodic sequence (y_n)
      - L is a real number
    """
    try:
        x, y, L = witness
    except Exception:
        return [False, False, False]
        
    # H1: (y_n) is a bounded sequence of real numbers
    # A periodic sequence given by a finite list is bounded.
    try:
        h1 = isinstance(y, (list, tuple, sympy.Tuple)) and len(y) > 0
        if h1:
            for yi in y:
                val = complex(sympy.sympify(yi))
                if val.imag != 0:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H2: S_y is the set of subsequential limits of (y_n)
    # This is true by definition, but we also verify that x is a valid sequence 
    # and L is a real number so the conclusion can be evaluated.
    try:
        h2 = isinstance(x, (list, tuple, sympy.Tuple)) and len(x) > 0
        if h2:
            for xi in x:
                val = complex(sympy.sympify(xi))
                if val.imag != 0:
                    h2 = False
                    break
            val_L = complex(sympy.sympify(L))
            if val_L.imag != 0:
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The set of subsequential limits of (x_n + y_n) is NOT equal to {L + s : s in S_y}
    try:
        n = len(x)
        m = len(y)
        lcm = (n * m) // math.gcd(n, m)
        
        S_x_plus_y = set()
        for i in range(lcm):
            val = sympy.sympify(x[i % n] + y[i % m], rational=True).simplify()
            S_x_plus_y.add(val)
            
        L_sym = sympy.sympify(L, rational=True)
        L_plus_Sy = set()
        for yi in y:
            val = sympy.sympify(L_sym + sympy.sympify(yi, rational=True)).simplify()
            L_plus_Sy.add(val)
            
        neg_q = S_x_plus_y != L_plus_Sy
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (y_n) is a bounded sequence of real numbers",
    "H_2: S_y is the set of subsequential limits of (y_n)",
    "¬Q: The set of subsequential limits of (x_n + y_n) is not equal to {L + s : s in S_y}"
]

N_HYP = 2
NEG_Q_INDEX = 2