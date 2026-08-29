import sympy
from sympy import Symbol

e = Symbol('e')

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring with identity
    try:
        R = witness.R
        if R in [sympy.ZZ, sympy.QQ]:
            H1 = True
        elif hasattr(R, 'is_commutative') and hasattr(R, 'has_Identity'):
            H1 = bool(R.is_commutative and R.has_Identity)
        elif hasattr(R, 'is_commutative'):
            H1 = bool(R.is_commutative)
        elif isinstance(R, int) and R > 1:
            H1 = True
        elif isinstance(R, str) and R.upper() in ["Z", "Q", "R", "C", "ZZ", "QQ"]:
            H1 = True
        else:
            H1 = False
    except Exception:
        H1 = False

    # H_2: D is the ring of dual numbers R[e]/(e^2) over R
    try:
        D = witness.D
        if isinstance(D, str):
            D_str = D.replace(" ", "").lower()
            H2 = any(sub in D_str for sub in ["dual", "e^2", "e**2", "d"])
        elif hasattr(D, 'is_dual_numbers'):
            H2 = bool(D.is_dual_numbers)
        else:
            H2 = D is not None
    except Exception:
        H2 = False

    # neg_Q: x is a unit in D if and only if a is a unit in R (must FAIL)
    try:
        x = witness.x
        a = witness.a
        R = witness.R
        
        def is_unit(val, ring):
            if hasattr(ring, 'is_unit'):
                try:
                    return bool(ring.is_unit(val))
                except Exception:
                    pass
            if ring == sympy.ZZ or (isinstance(ring, str) and ring.upper() in ["Z", "ZZ"]):
                return val in [1, -1]
            if ring == sympy.QQ or (isinstance(ring, str) and ring.upper() in ["Q", "QQ", "R", "C"]):
                return val != 0
            if isinstance(ring, int) and ring > 1:
                return sympy.gcd(val, ring) == 1
            if val in [1, -1]:
                return True
            return False

        # Extract the real part (u) of x in D
        if isinstance(x, (tuple, list)):
            u = x[0]
        elif hasattr(x, 'real_part'):
            u = x.real_part
        elif hasattr(x, 'subs'):
            e_sym = sympy.Symbol('e')
            u = x.subs(e_sym, 0)
        else:
            u = x

        x_is_unit = is_unit(u, R)
        a_is_unit = is_unit(a, R)
        
        neg_Q = (x_is_unit != a_is_unit)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: D is the ring of dual numbers over R",
    "neg_Q: x is a unit in D is not equivalent to a is a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2