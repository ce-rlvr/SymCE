import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _check_supersolvable(witness):
    if hasattr(witness, 'is_supersolvable'):
        val = witness.is_supersolvable
        return bool(val() if callable(val) else val)
        
    if hasattr(witness, 'is_solvable'):
        val = witness.is_solvable
        solvable = val() if callable(val) else val
        if not solvable:
            return False
            
    if hasattr(witness, 'chief_series'):
        val = witness.chief_series
        series = val() if callable(val) else val
        for i in range(len(series) - 1):
            idx = series[i].order() // series[i+1].order()
            if not isprime(idx):
                return False
        return True
        
    raise AttributeError("Cannot determine if supersolvable")

def _get_commutator_subgroup(witness):
    if hasattr(witness, 'commutator_subgroup'):
        val = witness.commutator_subgroup
        return val() if callable(val) else val
    if hasattr(witness, 'derived_subgroup'):
        val = witness.derived_subgroup
        return val() if callable(val) else val
    if hasattr(witness, 'derived_series'):
        val = witness.derived_series
        series = val() if callable(val) else val
        if len(series) > 1:
            return series[1]
        return series[0]
    raise AttributeError("No commutator subgroup found")

def _check_is_nilpotent(group):
    if hasattr(group, 'is_nilpotent'):
        val = group.is_nilpotent
        return bool(val() if callable(val) else val)
    raise AttributeError("No is_nilpotent attribute found")

def conditions(witness) -> list[bool]:
    try:
        h1_ok = _check_supersolvable(witness)
    except Exception:
        h1_ok = False
        
    try:
        C = _get_commutator_subgroup(witness)
        is_nilp = _check_is_nilpotent(C)
        neg_q_ok = not is_nilp
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a supersolvable group",
    "¬Q: The commutator subgroup G' is not nilpotent"
]

N_HYP = 1
NEG_Q_INDEX = 1