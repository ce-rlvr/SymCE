import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy import S

# Standard group bindings that might be used as witnesses for modules over Z
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Check if the witness is a counterexample to "Every module over a Euclidean domain is free."
    The witness can be a module M (implicitly over Z) or a tuple (R, M).
    M can be represented as an integer n (for Z/nZ), a list of invariant factors, 
    a presentation Matrix, or a PermutationGroup (finite abelian group).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R, M = S.Integers, witness
            
        is_euclidean = False
        if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            is_euclidean = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            is_euclidean = True
        elif hasattr(R, 'domain') and hasattr(R, 'gens'):
            if R.domain.is_Field and len(R.gens) == 1:
                is_euclidean = True
                
        if is_euclidean:
            if isinstance(M, (int, sympy.Integer)):
                h1 = True
            elif isinstance(M, list) and all(isinstance(x, (int, sympy.Integer)) for x in M):
                h1 = True
            elif isinstance(M, sympy.Matrix):
                h1 = True
            elif hasattr(M, "is_abelian"):
                h1 = bool(M.is_abelian)
            else:
                h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, M = witness
        else:
            M = witness
            
        if isinstance(M, (int, sympy.Integer)):
            neg_q = abs(M) > 1
        elif isinstance(M, list) and all(isinstance(x, (int, sympy.Integer)) for x in M):
            neg_q = any(abs(x) > 1 for x in M)
        elif isinstance(M, sympy.Matrix):
            from sympy.matrices.normalforms import smith_normal_form
            snf = smith_normal_form(M)
            neg_q = any(abs(snf[i, i]) > 1 for i in range(min(snf.rows, snf.cols)))
        elif hasattr(M, "order"):
            # A finite group is a free Z-module iff it is the trivial group
            neg_q = M.order() > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: M is not a free module"
]

N_HYP = 1
NEG_Q_INDEX = 1