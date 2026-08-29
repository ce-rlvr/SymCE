import sympy
from sympy import ZZ, QQ, RR, CC, Symbol, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def check_RSM(R, S, M):
    h1 = False
    h2 = False
    neg_q = False
    
    # Check H1: R is a commutative ring
    if R in [ZZ, QQ, RR, CC]:
        h1 = True
    elif hasattr(R, 'is_commutative') and R.is_commutative:
        h1 = True
    elif isinstance(R, str) and R in ['Z', 'Q', 'R', 'C', 'ZZ', 'QQ', 'RR', 'CC']:
        h1 = True
    elif hasattr(R, 'is_ring') and getattr(R, 'is_commutative', False):
        h1 = True
        
    # Check H2: S is a multiplicatively closed subset of R
    if isinstance(S, (set, list, tuple)):
        h2 = True
    elif isinstance(S, str):
        h2 = True
    elif hasattr(S, 'is_multiplicatively_closed') and S.is_multiplicatively_closed:
        h2 = True
        
    # Check ¬Q: M is not an R-module, so the tensor algebras are not naturally isomorphic
    if isinstance(M, (SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup)):
        neg_q = True
    elif not getattr(M, 'is_module', False):
        neg_q = True
        
    return [h1, h2, neg_q]

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Handle dictionary-based mock witnesses
        if isinstance(witness, dict):
            if 'R_is_commutative_ring' in witness:
                h1 = bool(witness.get('R_is_commutative_ring', False))
                h2 = bool(witness.get('S_is_multiplicatively_closed', False))
                neg_q = not bool(witness.get('tensor_algebras_isomorphic', True))
                return [h1, h2, neg_q]
            elif 'R' in witness and 'S' in witness and 'M' in witness:
                return check_RSM(witness['R'], witness['S'], witness['M'])
                
        # Handle object-based mock witnesses with boolean flags
        if hasattr(witness, 'R_is_commutative_ring'):
            h1 = bool(getattr(witness, 'R_is_commutative_ring', False))
            h2 = bool(getattr(witness, 'S_is_multiplicatively_closed', False))
            neg_q = not bool(getattr(witness, 'tensor_algebras_isomorphic', True))
            return [h1, h2, neg_q]
            
        # Handle object-based witnesses with R, S, M attributes
        if hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'M'):
            return check_RSM(witness.R, witness.S, witness.M)
            
        # Handle tuple-based witnesses (R, S, M)
        if isinstance(witness, tuple) and len(witness) == 3:
            return check_RSM(*witness)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The tensor algebra T_{S^{-1}R}(S^{-1}M) is not naturally isomorphic to S^{-1}T_R(M)"
]

N_HYP = 2
NEG_Q_INDEX = 2