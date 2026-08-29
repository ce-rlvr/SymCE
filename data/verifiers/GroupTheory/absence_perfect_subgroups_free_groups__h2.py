import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, free_group
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
        else:
            F, H = witness
    except Exception:
        return [False, False]
        
    # H_1: F is a free group
    try:
        h1 = False
        if type(F).__name__ == 'FreeGroup':
            h1 = True
        elif hasattr(F, 'relators') and len(F.relators) == 0:
            h1 = True
        elif hasattr(F, 'order'):
            if callable(F.order):
                if F.order() == 1:
                    h1 = True
            else:
                if F.order == 1:
                    h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: H is NOT the trivial group
    try:
        q = False
        
        if hasattr(H, 'order'):
            try:
                if callable(H.order):
                    if H.order() == 1:
                        q = True
                else:
                    if H.order == 1:
                        q = True
            except Exception:
                pass
                
        if not q and hasattr(H, 'is_trivial'):
            if H.is_trivial:
                q = True
                
        if not q and type(H).__name__ == 'FreeGroup':
            if len(H.generators) == 0:
                q = True
                
        if not q and hasattr(H, 'generators'):
            try:
                gens = H.generators
                if len(gens) == 0:
                    q = True
                else:
                    all_id = True
                    for g in gens:
                        if hasattr(g, 'is_identity'):
                            if not g.is_identity:
                                all_id = False
                                break
                        elif hasattr(g, 'is_Identity'):
                            if not g.is_Identity:
                                all_id = False
                                break
                        elif hasattr(g, 'group') and g == g.group.identity:
                            continue
                        else:
                            all_id = False
                            break
                    if all_id:
                        q = True
            except Exception:
                pass
                
        if not q and isinstance(H, (list, tuple, set)):
            if len(H) == 0:
                q = True
            else:
                all_id = True
                for g in H:
                    if hasattr(g, 'is_identity'):
                        if not g.is_identity:
                            all_id = False
                            break
                    elif hasattr(g, 'is_Identity'):
                        if not g.is_Identity:
                            all_id = False
                            break
                    elif hasattr(g, 'group') and g == g.group.identity:
                        continue
                    else:
                        all_id = False
                        break
                if all_id:
                    q = True
                    
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: H is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1