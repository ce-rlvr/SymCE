import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import npartitions

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

def conditions(witness):
    # H_1: p(n) denotes the number of integer partitions of n
    # This is a definitional hypothesis, so it holds as long as the witness is a valid group with a degree n.
    try:
        if not isinstance(witness, PermutationGroup):
            h1_ok = False
        else:
            n = witness.degree
            p_n = npartitions(n)
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The number of distinct conjugacy classes of G is NOT exactly p(n)
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q_ok = False
        else:
            n = witness.degree
            p_n = npartitions(n)
            
            try:
                # Try using the built-in property/method first
                cc = witness.conjugacy_classes
                if callable(cc):
                    num_classes = len(cc())
                else:
                    num_classes = len(cc)
            except Exception:
                # Fallback to manual computation for the number of conjugacy classes
                elements = list(witness.generate())
                classes = []
                seen = set()
                for g in elements:
                    if g not in seen:
                        c = set()
                        for h in elements:
                            conj = h * g * (~h)
                            c.add(conj)
                            seen.add(conj)
                        classes.append(c)
                num_classes = len(classes)
                
            neg_q_ok = bool(num_classes != p_n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p(n) denotes the number of integer partitions of n",
    "¬Q: The number of distinct conjugacy classes of G is not exactly p(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1