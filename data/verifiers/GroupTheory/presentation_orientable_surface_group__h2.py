import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            g = witness.get('g')
            G = witness.get('G')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            g, G = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(g, int) and g >= 1
    except Exception:
        h1 = False
        
    try:
        from sympy.combinatorics import PermutationGroup
        
        is_group = False
        if isinstance(G, PermutationGroup):
            is_group = True
        elif hasattr(G, 'generators') and hasattr(G, 'relators'):
            is_group = True
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            is_group = True
            
        if not is_group:
            neg_q = False
        else:
            neg_q = False
            
            if hasattr(G, 'is_finite') and G.is_finite:
                neg_q = True
            elif hasattr(G, 'order') and callable(G.order):
                try:
                    ord_G = G.order()
                    if ord_G != sympy.oo:
                        neg_q = True
                except Exception:
                    pass
                    
            if isinstance(G, PermutationGroup):
                neg_q = True
                
            if not neg_q and hasattr(G, 'generators') and hasattr(G, 'relators'):
                if len(G.generators) == 2 * g and len(G.relators) == 1:
                    neg_q = False
                else:
                    neg_q = True
                    
            if not neg_q and not (hasattr(G, 'generators') and hasattr(G, 'relators')):
                neg_q = True
                
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S_g is a closed, connected, orientable surface of genus g >= 1",
    "not_Q: G does not admit the presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1