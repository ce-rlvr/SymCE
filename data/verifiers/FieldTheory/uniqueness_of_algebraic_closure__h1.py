import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness satisfies the remaining hypotheses and fails the conclusion.
    Since algebraic closures of arbitrary rings are not natively represented in SymPy,
    the witness is expected to be a custom object, dictionary, or tuple that provides
    the necessary properties or methods.
    """
    h1 = False
    try:
        if hasattr(witness, 'K1_is_algebraic_closure_of_F'):
            val = witness.K1_is_algebraic_closure_of_F
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_algebraic_closure'):
            h1 = bool(witness.is_algebraic_closure(witness.K1, witness.F))
        elif isinstance(witness, dict) and 'K1_is_algebraic_closure_of_F' in witness:
            h1 = bool(witness['K1_is_algebraic_closure_of_F'])
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            F, K1, K2 = witness
            if hasattr(K1, 'is_algebraic_closure'):
                h1 = bool(K1.is_algebraic_closure(F))
    except Exception:
        pass

    h2 = False
    try:
        if hasattr(witness, 'K2_is_algebraic_closure_of_F'):
            val = witness.K2_is_algebraic_closure_of_F
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_algebraic_closure'):
            h2 = bool(witness.is_algebraic_closure(witness.K2, witness.F))
        elif isinstance(witness, dict) and 'K2_is_algebraic_closure_of_F' in witness:
            h2 = bool(witness['K2_is_algebraic_closure_of_F'])
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            F, K1, K2 = witness
            if hasattr(K2, 'is_algebraic_closure'):
                h2 = bool(K2.is_algebraic_closure(F))
    except Exception:
        pass

    neg_q = False
    try:
        if hasattr(witness, 'exists_isomorphism_fixing_F'):
            val = witness.exists_isomorphism_fixing_F
            q = bool(val() if callable(val) else val)
            neg_q = not q
        elif hasattr(witness, 'is_isomorphic_fixing'):
            q = bool(witness.is_isomorphic_fixing(witness.K1, witness.K2, witness.F))
            neg_q = not q
        elif isinstance(witness, dict) and 'exists_isomorphism_fixing_F' in witness:
            q = bool(witness['exists_isomorphism_fixing_F'])
            neg_q = not q
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            F, K1, K2 = witness
            if hasattr(K1, 'is_isomorphic_to'):
                q = bool(K1.is_isomorphic_to(K2, fixing=F))
                neg_q = not q
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K1 is an algebraic closure of F",
    "H_2: K2 is an algebraic closure of F",
    "¬Q: There does not exist a field isomorphism from K1 to K2 that fixes every element of F"
]

N_HYP = 2
NEG_Q_INDEX = 2