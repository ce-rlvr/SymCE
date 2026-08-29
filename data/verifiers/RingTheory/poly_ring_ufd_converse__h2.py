import sympy
from sympy import symbols, Rational, Integer
from sympy.polys.domains import ZZ, QQ

# Define common counterexamples as custom objects for convenience
class _Ring:
    def __init__(self, name, is_domain, is_ufd):
        self.name = name
        self.is_Domain = is_domain
        self.is_UFD = is_ufd
        self.is_Field = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

Z_sqrt_m5 = _Ring("Z[sqrt(-5)]", True, False)
Z_sqrt_m3 = _Ring("Z[sqrt(-3)]", True, False)
Z_x_y_z_w_mod_xy_zw = _Ring("Z[x,y,z,w]/(xy-zw)", True, False)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Check H_1: R is an integral domain
    try:
        if type(witness).__name__ == 'QuotientRing':
            s = str(witness).replace(" ", "").lower()
            if ("x**2" in s or "x^2" in s) and "+" not in s and "-" not in s:
                h1 = False
            else:
                h1 = True
        elif hasattr(witness, 'is_Domain'):
            h1 = bool(witness.is_Domain)
        elif hasattr(witness, 'is_integral_domain'):
            h1 = bool(witness.is_integral_domain)
        else:
            s = str(witness).replace(" ", "").lower()
            if "z/" in s and any(n in s for n in ["4", "6", "8", "9", "10", "12"]):
                h1 = False
            elif ("x**2" in s or "x^2" in s) and "+" not in s and "-" not in s:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # Check ¬Q: R is not a Unique Factorization Domain
    try:
        if hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        elif type(witness).__name__ == 'QuotientRing':
            s = str(witness).replace(" ", "").lower()
            non_ufds = ["xy-zw", "x*y-z*w", "x**2+5", "x^2+5"]
            if any(n in s for n in non_ufds):
                neg_q = True
            else:
                neg_q = False
        elif hasattr(witness, 'is_UFD'):
            neg_q = not bool(witness.is_UFD)
        elif hasattr(witness, 'is_ufd'):
            neg_q = not bool(witness.is_ufd)
        else:
            s = str(witness).replace(" ", "").lower()
            if "q[" in s and "sqrt" in s:
                neg_q = False
            else:
                non_ufds = [
                    "sqrt(-5)", "sqrt(-3)", "sqrt(-6)", "sqrt(-7)", 
                    "sqrt(-10)", "sqrt(-13)", "sqrt(-14)", "sqrt(-15)", 
                    "sqrt(-17)", "xy-zw", "x*y-z*w"
                ]
                if any(n in s for n in non_ufds):
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a Unique Factorization Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1