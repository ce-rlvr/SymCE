import math
import sympy
from sympy.abc import x

# Top-level setup
# The witness is expected to be a tuple: (m, f_dict, g_dict)
# where:
#   - m is an integer >= 2, representing the ring R = Z/mZ
#   - f_dict is a dictionary {degree: coefficient} representing the Laurent series f(x)
#   - g_dict is a dictionary {degree: coefficient} representing g(x), the inverse of f(x)

def conditions(witness):
    try:
        m, f_dict, g_dict = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a ring (we use Z/mZ, so m >= 2)
    try:
        h1 = isinstance(m, int) and m >= 2
    except Exception:
        h1 = False
        
    # H2: f(x) is a non-zero formal Laurent series in R((x))
    try:
        f_clean = {int(d): int(c) % m for d, c in f_dict.items() if int(c) % m != 0}
        h2 = len(f_clean) > 0
    except Exception:
        h2 = False
        
    # neg_Q: f(x) is a unit in R((x)) but its lowest degree non-zero coefficient is not a unit in R
    try:
        if not h2:
            neg_q = False
        else:
            k = min(f_clean.keys())
            ak = f_clean[k]
            is_unit_ak = math.gcd(ak, m) == 1
            
            g_clean = {int(d): int(c) % m for d, c in g_dict.items() if int(c) % m != 0}
            
            # Compute the product of f(x) and g(x) in R((x))
            prod = {}
            for df, cf in f_clean.items():
                for dg, cg in g_clean.items():
                    deg = df + dg
                    prod[deg] = (prod.get(deg, 0) + cf * cg) % m
                    
            prod_clean = {d: c for d, c in prod.items() if c != 0}
            is_unit_f = (prod_clean == {0: 1})
            
            neg_q = is_unit_f and not is_unit_ak
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: f(x) is a non-zero formal Laurent series in R((x))",
    "¬Q: f(x) is a unit in R((x)) but its lowest degree non-zero coefficient is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2