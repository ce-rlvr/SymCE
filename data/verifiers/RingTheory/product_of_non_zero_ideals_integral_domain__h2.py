import sympy
from sympy import sympify
from sympy.polys.domains import Domain, ZZ, QQ, RR, CC

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: J is a non-zero ideal of R",
    "¬Q: The product ideal IJ is zero"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                R = ZZ
                I, J = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if hasattr(I, 'gens'):
            I = I.gens
        elif not isinstance(I, (list, tuple, set)):
            I = [I]
            
        if hasattr(J, 'gens'):
            J = J.gens
        elif not isinstance(J, (list, tuple, set)):
            J = [J]
    except Exception:
        return [False, False, False]

    # H_1: R is an integral domain
    try:
        if R == sympy.S.Integers:
            R = ZZ
        elif R == sympy.S.Rationals:
            R = QQ
        elif R == sympy.S.Reals:
            R = RR
        elif R == sympy.S.Complexes:
            R = CC
            
        # In SymPy, Domain instances represent integral domains.
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    # Helper to convert elements to the ring R
    def to_R(val):
        try:
            if R.of_type(val):
                return val
        except Exception:
            pass
        return R.from_sympy(sympify(val))

    # H_2: J is a non-zero ideal of R
    try:
        J_elements = [to_R(j) for j in J]
        h2 = any(j != R.zero for j in J_elements)
    except Exception:
        h2 = False

    # ¬Q: The product ideal IJ is zero
    try:
        I_elements = [to_R(i) for i in I]
        J_elements = [to_R(j) for j in J]
        
        neg_q = True
        for i in I_elements:
            for j in J_elements:
                if R.mul(i, j) != R.zero:
                    neg_q = False
                    break
            if not neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]