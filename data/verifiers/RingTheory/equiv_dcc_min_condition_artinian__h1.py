import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.agca.modules import Module

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    Since the equivalence of DCC and the minimal condition is a theorem in ZFC for any poset 
    (and thus for the poset of submodules of any module), there are no true counterexamples.
    This verifier safely evaluates properties if the witness provides them.
    """
    h1 = False
    neg_q = False
    
    try:
        # Check if M is a left or right R-module
        if isinstance(witness, Module):
            h1 = True
        elif hasattr(witness, 'is_module'):
            h1 = bool(witness.is_module)
        elif witness in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
    except Exception:
        pass

    try:
        # Check if DCC is NOT equivalent to the minimal condition
        if hasattr(witness, 'satisfies_dcc') and hasattr(witness, 'satisfies_minimal_condition'):
            dcc = bool(witness.satisfies_dcc)
            min_cond = bool(witness.satisfies_minimal_condition)
            neg_q = (dcc != min_cond)
        elif hasattr(witness, 'is_artinian') and hasattr(witness, 'has_minimal_condition'):
            dcc = bool(witness.is_artinian)
            min_cond = bool(witness.has_minimal_condition)
            neg_q = (dcc != min_cond)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a left or right R-module",
    "¬Q: M satisfies DCC on submodules is NOT equivalent to every non-empty collection of submodules having a minimal element"
]

N_HYP = 1
NEG_Q_INDEX = 1