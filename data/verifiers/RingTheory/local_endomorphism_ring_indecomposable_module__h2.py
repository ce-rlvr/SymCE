import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint
from sympy import eye, zeros

# Top-level setup for potential witness expressions
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
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If M has finite length as an R-module, then End_R(M) is a local ring."
    
    The witness can be:
    - An integer n > 0, representing the Z-module Z/nZ.
    - A list/tuple of integers > 0, representing a direct sum of cyclic Z-modules.
    - A sympy PermutationGroup (must be abelian to be a Z-module).
    """
    try:
        h1 = False
        h2 = False
        neg_q = False
        
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True  # R = Z is a ring
            h2 = witness > 0  # Z/nZ has finite length as a Z-module
            if h2:
                # End(Z/nZ) is local iff Z/nZ is indecomposable iff n is a prime power
                is_local = (witness > 1) and (len(factorint(witness)) == 1)
                neg_q = not is_local
                
        elif isinstance(witness, (list, tuple)):
            h1 = True
            h2 = all(isinstance(x, (int, sympy.Integer)) and x > 0 for x in witness)
            if h2:
                # A finite abelian group is indecomposable iff it's a single cyclic p-group
                if len(witness) == 1:
                    n = witness[0]
                    is_local = (n > 1) and (len(factorint(n)) == 1)
                else:
                    is_local = False
                neg_q = not is_local
                
        elif hasattr(witness, 'is_abelian') and hasattr(witness, 'order'):
            if witness.is_abelian:
                h1 = True
                h2 = True
                order = witness.order()
                if order > 1:
                    is_p_group = len(factorint(order)) == 1
                    is_cyclic = getattr(witness, 'is_cyclic', None)
                    if is_cyclic is None:
                        if hasattr(witness, 'generate'):
                            is_cyclic = any(g.order() == order for g in witness.generate())
                        else:
                            is_cyclic = False
                    is_local = is_p_group and is_cyclic
                else:
                    is_local = False
                neg_q = not is_local
                
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M has finite length as an R-module",
    "¬Q: The endomorphism ring End_R(M) is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2