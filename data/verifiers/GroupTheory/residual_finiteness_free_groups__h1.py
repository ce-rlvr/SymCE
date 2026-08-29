import sympy
from sympy import S
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
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
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, g = witness
        else:
            F = witness.F
            g = witness.g
    except Exception:
        return [False, False]
        
    # H_1: g is an element of F such that g is not the identity
    h1_ok = False
    try:
        if hasattr(F, '__contains__'):
            in_F = g in F
        elif isinstance(F, (list, tuple, set)):
            in_F = g in F
        else:
            in_F = True
            
        ident = None
        if hasattr(F, 'identity'):
            ident = F.identity
        elif hasattr(F, 'zero'):
            ident = F.zero
        elif F in (S.Rationals, S.Reals, S.Complexes, S.Integers):
            ident = 0
            
        if ident is not None:
            not_ident = (g != ident)
        else:
            not_ident = (g != 0 and g != 1)
            
        h1_ok = bool(in_F and not_ident)
    except Exception:
        h1_ok = False
        
    # neg_Q: Every normal subgroup of F of finite index contains g
    neg_q_ok = False
    try:
        if hasattr(F, 'has_finite_index_normal_subgroup_excluding'):
            neg_q_ok = not F.has_finite_index_normal_subgroup_excluding(g)
        elif hasattr(F, 'is_PermutationGroup') and F.is_PermutationGroup:
            # Finite groups are residually finite
            neg_q_ok = False
        elif isinstance(F, (list, tuple, set)):
            # Finite collections are residually finite
            neg_q_ok = False
        elif F in (S.Rationals, S.Reals, S.Complexes):
            # Divisible groups have no proper finite index subgroups,
            # so the only finite index subgroup is F itself, which contains g.
            neg_q_ok = True
        elif F == S.Integers:
            # The integers are residually finite
            neg_q_ok = False
        else:
            # If we cannot determine, assume it's not a counterexample
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: g is an element of F such that g is not the identity",
    "¬Q: Every normal subgroup of F of finite index contains g"
]

N_HYP = 1
NEG_Q_INDEX = 1