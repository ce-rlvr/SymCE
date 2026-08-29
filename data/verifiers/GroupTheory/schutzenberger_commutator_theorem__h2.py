import sympy
import sympy.combinatorics

# Top-level setup
try:
    F2, a, b = sympy.combinatorics.free_group("a, b")
except Exception:
    F2, a, b = None, None, None

def conditions(witness):
    try:
        if len(witness) == 5:
            F, z, n, x, y = witness
        elif len(witness) == 4:
            z, n, x, y = witness
            F = z.group
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
    
    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup' or (
            hasattr(sympy.combinatorics, 'FreeGroup') and isinstance(F, sympy.combinatorics.FreeGroup)
        )
    except Exception:
        h1 = False

    # H_2: z in F
    try:
        h2 = hasattr(z, 'group') and z.group == F
    except Exception:
        h2 = False

    # H_3: n is an integer such that z^n = commutator of x and y
    try:
        is_int = isinstance(n, (int, sympy.Integer))
        n_val = int(n) if is_int else n
        in_F = hasattr(x, 'group') and x.group == F and hasattr(y, 'group') and y.group == F
        
        # Commutator can be defined as x^-1 y^-1 x y or x y x^-1 y^-1
        comm1 = (x**-1) * (y**-1) * x * y
        comm2 = x * y * (x**-1) * (y**-1)
        
        h3 = is_int and in_F and (z**n_val == comm1 or z**n_val == comm2)
    except Exception:
        h3 = False

    # neg_Q: n != 1 and n != -1
    try:
        n_val = int(n)
        neg_q = n_val not in (1, -1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: z in F",
    "H_3: n is an integer such that z^n is the commutator of x and y",
    "¬Q: n != 1 and n != -1"
]

N_HYP = 3
NEG_Q_INDEX = 3