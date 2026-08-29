import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    h1_ok = False
    neg_q = False
    
    try:
        if hasattr(witness, 'H1'):
            h1_ok = bool(witness.H1() if callable(witness.H1) else witness.H1)
        elif hasattr(witness, 'is_generating_set'):
            h1_ok = bool(witness.is_generating_set() if callable(witness.is_generating_set) else witness.is_generating_set)
        else:
            if isinstance(witness, tuple) and len(witness) == 2:
                G, S = witness
            else:
                G = witness.G
                S = witness.S
                
            if hasattr(G, 'is_generated_by'):
                h1_ok = bool(G.is_generated_by(S))
            elif isinstance(G, PermutationGroup):
                try:
                    H = PermutationGroup(*S)
                except Exception:
                    H = PermutationGroup(S)
                h1_ok = (H == G)
            elif hasattr(G, 'generators'):
                h1_ok = (set(S) == set(G.generators))
    except Exception:
        pass

    try:
        if hasattr(witness, 'neg_Q'):
            neg_q = bool(witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q)
        else:
            if isinstance(witness, tuple) and len(witness) == 2:
                G, S = witness
            else:
                G = witness.G
                S = witness.S
                
            is_grp = False
            if isinstance(G, PermutationGroup):
                is_grp = True
            elif hasattr(G, 'is_group') and G.is_group:
                is_grp = True
            elif type(G).__name__ in ['FpGroup', 'FreeGroup', 'AlternatingGroup', 'SymmetricGroup', 'CyclicGroup', 'DihedralGroup']:
                is_grp = True
            
            neg_q = not is_grp
    except Exception:
        pass

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: S is a generating set for G",
    "¬Q: There does not exist a free group F on a set of the same cardinality as S and a surjective group homomorphism from F onto G"
]

N_HYP = 1
NEG_Q_INDEX = 1