import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: G is a torsion-free abelian group",
    "¬Q: The group ring is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        # Extract R and G
        if isinstance(witness, dict):
            R = witness.get('R')
            G = witness.get('G')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, G = witness
        else:
            R = getattr(witness, 'R', None)
            G = getattr(witness, 'G', None)
            
        if R is not None and G is not None:
            # Check H1: R is an integral domain
            if hasattr(R, 'is_domain'):
                h1 = R.is_domain() if callable(R.is_domain) else R.is_domain
            elif hasattr(R, 'is_integral_domain'):
                h1 = R.is_integral_domain() if callable(R.is_integral_domain) else R.is_integral_domain
            elif R in [ZZ, QQ]:
                h1 = True
                
            # Check H2: G is a torsion-free abelian group
            is_ab = False
            if hasattr(G, 'is_abelian'):
                is_ab = G.is_abelian() if callable(G.is_abelian) else G.is_abelian
            elif G in [ZZ, QQ]:
                is_ab = True
                
            is_tf = False
            if hasattr(G, 'is_torsion_free'):
                is_tf = G.is_torsion_free() if callable(G.is_torsion_free) else G.is_torsion_free
            elif G in [ZZ, QQ]:
                is_tf = True
            elif hasattr(G, 'order'):
                order = G.order() if callable(G.order) else G.order
                if order == 1:
                    is_tf = True
            
            h2 = bool(is_ab and is_tf)
            
            # Check Q: R[G] is an integral domain
            is_R_comm = False
            if hasattr(R, 'is_commutative'):
                is_R_comm = R.is_commutative() if callable(R.is_commutative) else R.is_commutative
            elif R in [ZZ, QQ]:
                is_R_comm = True
                
            q = bool(h1 and h2 and is_R_comm)
            neg_q = not q
            
    except Exception:
        pass
        
    # Fallback for mock objects
    try:
        if hasattr(witness, 'R_is_integral_domain'):
            h1 = witness.R_is_integral_domain
        if hasattr(witness, 'G_is_torsion_free_abelian'):
            h2 = witness.G_is_torsion_free_abelian
        if hasattr(witness, 'RG_is_integral_domain'):
            neg_q = not witness.RG_is_integral_domain
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]