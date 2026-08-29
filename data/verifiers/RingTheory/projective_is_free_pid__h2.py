import sympy
from sympy import Matrix, eye, zeros, S
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x

class NamedModule:
    def __init__(self, name, ring, is_free):
        self.name = name
        self.ring = ring
        self.is_free = is_free
    def __repr__(self):
        return self.name

# Standard modules over ZZ for easy witness construction
Z2_mod = NamedModule("Z/2Z", ZZ, False)
Z3_mod = NamedModule("Z/3Z", ZZ, False)
Q_mod = NamedModule("Q", ZZ, False)
Z_mod = NamedModule("Z", ZZ, True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, M) where R is a ring and M is a module.
    M can be a NamedModule, a presentation Matrix, a list of invariant factors, or a string.
    """
    R = None
    M = None
    
    if isinstance(witness, NamedModule):
        R = witness.ring
        M = witness
    elif isinstance(witness, tuple) and len(witness) == 2:
        R, M = witness
    else:
        return [False, False]
        
    # H_1: R is a principal ideal domain
    h1 = False
    try:
        if hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID)
        elif R in [ZZ, QQ, S.Integers, S.Rationals]:
            h1 = True
        elif str(R) in ["ZZ", "Z", "Integers", "QQ", "Q", "Rationals"]:
            h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: M is NOT a free R-module
    neg_q = False
    try:
        if isinstance(M, NamedModule):
            if R in [QQ, S.Rationals] or str(R) in ["QQ", "Q", "Rationals"]:
                neg_q = False  # Modules over a field are vector spaces (free)
            else:
                neg_q = not M.is_free
        elif isinstance(M, Matrix):
            # M is interpreted as a presentation matrix over R
            if R in [ZZ, S.Integers] or str(R) in ["ZZ", "Z", "Integers"]:
                snf = M.smith_normal_form()
                is_free = True
                for i in range(min(snf.rows, snf.cols)):
                    val = abs(snf[i, i])
                    # A finitely generated module over Z is free iff its invariant factors are 1 or 0
                    if val != 0 and val != 1:
                        is_free = False
                        break
                neg_q = not is_free
            elif R in [QQ, S.Rationals] or str(R) in ["QQ", "Q", "Rationals"]:
                neg_q = False
        elif M in [QQ, S.Rationals]:
            if R in [ZZ, S.Integers] or str(R) in ["ZZ", "Z", "Integers"]:
                neg_q = True
        elif isinstance(M, str):
            M_str = M.replace(" ", "").lower()
            if any(sub in M_str for sub in ["z/2", "z_2", "z2", "q", "torsion", "z/3", "z_3", "z3", "z/n"]):
                neg_q = True
            elif M_str in ["z", "z^2", "z^3"]:
                neg_q = False
        elif isinstance(M, list):
            # M is interpreted as a list of invariant factors
            is_free = True
            for val in M:
                try:
                    v = abs(int(val))
                    if v != 0 and v != 1:
                        is_free = False
                        break
                except Exception:
                    pass
            neg_q = not is_free
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: M is not a free R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1