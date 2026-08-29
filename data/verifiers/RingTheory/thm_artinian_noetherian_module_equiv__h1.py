import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

class Module:
    def __init__(self, name, is_right_module, is_artinian, is_noetherian):
        self.name = name
        self.is_right_module = bool(is_right_module)
        self.is_artinian = bool(is_artinian)
        self.is_noetherian = bool(is_noetherian)
        
    def __repr__(self):
        return f"Module({self.name})"

# Predefined standard modules for testing the conjecture
Z = Module("Z", True, False, True)
Q = Module("Q", True, True, True)
Z_p_infty = Module("Z_p_infty", True, True, False)
Qx = Module("Qx", True, False, True)
Free_inf = Module("Free_inf", True, False, False)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # Witness can be a module M, or a tuple (M, R)
        if isinstance(witness, tuple) and len(witness) >= 1:
            M = witness[0]
        else:
            M = witness
            
        if isinstance(M, Module):
            h1 = M.is_right_module
            art = M.is_artinian
            noeth = M.is_noetherian
        elif M == ZZ:
            h1 = True
            art = False
            noeth = True
        elif M == QQ:
            h1 = True
            art = True
            noeth = True
        elif isinstance(M, str):
            if M in ("Z", "ZZ"):
                h1, art, noeth = True, False, True
            elif M in ("Q", "QQ"):
                h1, art, noeth = True, True, True
            elif M == "Z_p_infty":
                h1, art, noeth = True, True, False
            else:
                h1, art, noeth = False, False, False
        else:
            h1 = False
            art = False
            noeth = False
            
        # The conclusion is "M is Artinian iff M is Noetherian"
        # The negation is that one is true and the other is false.
        neg_q = (art != noeth)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a right R-module",
    "¬Q: M is Artinian but not Noetherian, or Noetherian but not Artinian"
]

N_HYP = 1
NEG_Q_INDEX = 1