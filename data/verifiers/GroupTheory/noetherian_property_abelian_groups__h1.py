import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        # P: G is finitely generated
        # In SymPy, standard group objects (PermutationGroup, FreeGroup, FpGroup) 
        # are finitely generated and expose a 'generators' attribute.
        if hasattr(witness, 'generators'):
            P = True
        else:
            # If we cannot confirm it is finitely generated, we cannot evaluate it.
            # Note: If P is False, Q (Noetherian) must also be False, so P == Q would be True,
            # meaning the conclusion holds and it cannot be a counterexample.
            return [False]
            
        # Q: every strictly ascending chain of subgroups is finite (Noetherian property)
        if isinstance(witness, PermutationGroup):
            # Finite groups are always Noetherian
            Q = True
        elif type(witness).__name__ == 'FreeGroup':
            # A free group is Noetherian if and only if its rank is 0 or 1
            Q = len(witness.generators) <= 1
        elif type(witness).__name__ == 'FpGroup':
            if len(witness.relators) == 0:
                Q = len(witness.generators) <= 1
            else:
                # For an arbitrary finitely presented group, deciding the Noetherian property is undecidable.
                # To avoid false positives (accepting a valid theorem instance as a counterexample),
                # we conservatively assume Q is True.
                Q = True
        else:
            Q = True
            
        # The conclusion is P <-> Q. It fails when P != Q.
        neg_Q = (P != Q)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: G is finitely generated iff every strictly ascending chain of subgroups is finite (fails)"
]

N_HYP = 0
NEG_Q_INDEX = 0