import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    # H_1: The cardinality of \Omega is at least 2
    try:
        if hasattr(witness, "degree"):
            deg = witness.degree
        elif hasattr(witness, "domain_size"):
            deg = witness.domain_size
        elif hasattr(witness, "domain"):
            deg = len(witness.domain)
        else:
            deg = len(witness)
        h1 = bool(deg >= 2)
    except Exception:
        h1 = False

    # H_2: The action of G on \Omega is transitive
    try:
        if hasattr(witness, "is_transitive"):
            if callable(witness.is_transitive):
                h2 = bool(witness.is_transitive())
            else:
                h2 = bool(witness.is_transitive)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: For all g \in G, there exists \alpha \in \Omega such that g(\alpha) == \alpha
    # (i.e., no element is a derangement)
    try:
        if hasattr(witness, "has_derangement"):
            if callable(witness.has_derangement):
                has_der = bool(witness.has_derangement())
            else:
                has_der = bool(witness.has_derangement)
            neg_q = not has_der
        elif hasattr(witness, "is_derangement_free"):
            if callable(witness.is_derangement_free):
                neg_q = bool(witness.is_derangement_free())
            else:
                neg_q = bool(witness.is_derangement_free)
        else:
            has_der = False
            count = 0
            # Fallback for finite groups (e.g. SymPy PermutationGroup)
            for g in witness.elements:
                count += 1
                if count > 10000:
                    break
                
                is_der = True
                for i in range(int(deg)):
                    try:
                        val = g(i)
                    except TypeError:
                        val = g[i]
                    
                    if val == i:
                        is_der = False
                        break
                
                if is_der:
                    has_der = True
                    break
            neg_q = not has_der
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The cardinality of Omega is at least 2",
    "H_2: The action of G on Omega is transitive",
    "¬Q: Every element of G has at least one fixed point (no derangement exists)"
]

N_HYP = 2
NEG_Q_INDEX = 2