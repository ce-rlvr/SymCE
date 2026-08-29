import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is torsion-free",
    "H_2: The rank of G is 1",
    "¬Q: G is not isomorphic to a subgroup of Q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: G is torsion-free
    h1 = False
    try:
        if isinstance(witness, dict) and 'is_torsion_free' in witness:
            h1 = bool(witness['is_torsion_free'])
        elif hasattr(witness, 'is_torsion_free'):
            val = witness.is_torsion_free
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'relators'):
            # Heuristic for SymPy FpGroup: 
            # A 1-relator group is torsion-free iff its relator is not a proper power.
            if len(witness.relators) == 0:
                h1 = True
            elif len(witness.relators) == 1:
                r = witness.relators[0]
                if hasattr(r, 'letter_form'):
                    word = r.letter_form
                    n = len(word)
                    is_power = False
                    for i in range(1, n // 2 + 1):
                        if n % i == 0:
                            if word[:i] * (n // i) == word:
                                is_power = True
                                break
                    h1 = not is_power
                else:
                    h1 = True
    except Exception:
        pass

    # H_2: The rank of G is 1
    h2 = False
    try:
        if isinstance(witness, dict) and 'rank' in witness:
            h2 = witness['rank'] == 1
        elif hasattr(witness, 'rank'):
            val = witness.rank
            h2 = (val() if callable(val) else val) == 1
        elif hasattr(witness, 'abelian_invariants'):
            # For FpGroup, the torsion-free rank is the number of 0s in abelian invariants
            invs = witness.abelian_invariants()
            h2 = invs.count(0) == 1
    except Exception:
        pass

    # ¬Q: G is not isomorphic to a subgroup of Q
    # Any subgroup of Q is abelian. Since G is torsion-free and rank 1 (by H1, H2),
    # it fails to be a subgroup of Q if and only if it is not abelian.
    neg_q = False
    try:
        if isinstance(witness, dict) and 'is_isomorphic_to_subgroup_of_Q' in witness:
            neg_q = not bool(witness['is_isomorphic_to_subgroup_of_Q'])
        elif isinstance(witness, dict) and 'is_abelian' in witness:
            neg_q = not bool(witness['is_abelian'])
        elif hasattr(witness, 'is_isomorphic_to_subgroup_of_Q'):
            val = witness.is_isomorphic_to_subgroup_of_Q
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_abelian'):
            val = witness.is_abelian
            neg_q = not bool(val() if callable(val) else val)
    except Exception:
        pass

    return [h1, h2, neg_q]