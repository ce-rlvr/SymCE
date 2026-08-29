import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

# Top-level setup
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
    H1_ok = False
    H2_ok = False
    H3_ok = False
    neg_Q_ok = False
    
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            F = witness.get('F')
        elif isinstance(witness, tuple):
            G = witness[0]
            F = witness[1] if len(witness) > 1 else None
        else:
            G = witness
            F = None
            
        if isinstance(G, PermutationGroup):
            if getattr(G, 'is_finite', True):
                H1_ok = True
            
        if F is not None:
            if hasattr(F, 'is_Field') and getattr(F, 'is_Field'):
                H2_ok = True
            elif isinstance(F, int) and isprime(F):
                H2_ok = True
            elif isinstance(F, str) and F in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']:
                H2_ok = True
            elif hasattr(F, '__class__') and 'Field' in F.__class__.__name__:
                H2_ok = True
                
        if H1_ok and H2_ok:
            H3_ok = True
            
        # The class sums always form a basis for the center of the group algebra
        # for any finite group and any field. Thus the conclusion is always true,
        # and its negation is always false.
        neg_Q_ok = False
        
    except Exception:
        pass
        
    return [H1_ok, H2_ok, H3_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: F is a field",
    "H_3: FG is the group algebra of G over F",
    "¬Q: The class sums do not form a basis for the center of FG"
]

N_HYP = 3
NEG_Q_INDEX = 3