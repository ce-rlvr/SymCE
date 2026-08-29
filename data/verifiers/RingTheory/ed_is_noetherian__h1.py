import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ, EX

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        neg_q = False
        if hasattr(witness, 'is_Noetherian'):
            if witness.is_Noetherian is False:
                neg_q = True
        
        if not neg_q and hasattr(witness, 'gens'):
            try:
                if len(witness.gens) == float('inf'):
                    neg_q = True
            except Exception:
                pass
                
        if not neg_q and str(witness) == 'EX':
            neg_q = True
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: Every ascending chain of ideals in R does not eventually stabilize (R is not Noetherian)"]
N_HYP = 0
NEG_Q_INDEX = 0