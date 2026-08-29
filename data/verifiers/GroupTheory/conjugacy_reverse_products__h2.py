import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False]
        G, x, y = witness
    except Exception:
        return [False, False]
        
    # H1: G is a group
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            h1 = True
        elif hasattr(G, 'is_group') and getattr(G, 'is_group'):
            h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: xy is NOT conjugate to yx in G
    try:
        xy = x * y
        yx = y * x
        
        is_conj = False
        action_successful = False
        
        if hasattr(G, 'elements'):
            elements = G.elements
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = G  # Fallback if G is an iterable of elements
            
        for g in elements:
            try:
                try:
                    ginv = ~g
                except Exception:
                    ginv = g**-1
                    
                conj1 = g * xy * ginv
                conj2 = ginv * xy * g
                action_successful = True
                
                if conj1 == yx or conj2 == yx:
                    is_conj = True
                    break
            except Exception:
                continue
                
        if not action_successful:
            neg_q = False
        else:
            neg_q = not is_conj
            
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The product xy is not conjugate to the product yx in G"
]

N_HYP = 1
NEG_Q_INDEX = 1