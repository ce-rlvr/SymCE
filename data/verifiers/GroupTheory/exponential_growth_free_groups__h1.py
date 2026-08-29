import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        k = None
        r = None
        
        if isinstance(witness, dict):
            k = witness.get('k')
            S = witness.get('S')
            F = witness.get('F')
            if S is not None:
                if isinstance(S, int): 
                    r = S
                elif hasattr(S, '__len__'): 
                    r = len(S)
            elif F is not None:
                if hasattr(F, 'generators'): 
                    r = len(F.generators)
                elif hasattr(F, 'rank'): 
                    r = F.rank
            elif 'r' in witness:
                r = witness['r']
        elif isinstance(witness, tuple):
            if len(witness) > 0:
                k = witness[0]
            if len(witness) == 2:
                S = witness[1]
                if isinstance(S, int): 
                    r = S
                elif hasattr(S, 'generators'): 
                    r = len(S.generators)
                elif hasattr(S, '__len__'): 
                    r = len(S)
            elif len(witness) >= 3:
                S = witness[1]
                if isinstance(S, int): 
                    r = S
                elif hasattr(S, 'generators'): 
                    r = len(S.generators)
                elif hasattr(S, '__len__'): 
                    r = len(S)
                else:
                    S = witness[2]
                    if isinstance(S, int): 
                        r = S
                    elif hasattr(S, 'generators'): 
                        r = len(S.generators)
                    elif hasattr(S, '__len__'): 
                        r = len(S)
        
        if k is not None:
            try:
                h1 = (int(k) >= 2)
            except Exception:
                h1 = False
                
        if r is not None:
            try:
                h2 = (int(r) >= 0)
                # The word growth function of a free group of rank r is strictly exponential iff r >= 2.
                # If r <= 1, the growth is polynomial (linear for r=1, constant for r=0).
                neg_q = (int(r) <= 1)
            except Exception:
                h2 = False
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k >= 2",
    "H_2: S is a finite free generating set for F",
    "¬Q: The word growth function of F with respect to S is not strictly exponential"
]

N_HYP = 2
NEG_Q_INDEX = 2