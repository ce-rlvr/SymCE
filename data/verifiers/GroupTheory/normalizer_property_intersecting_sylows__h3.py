import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            Q = witness.get('Q')
        else:
            if len(witness) == 4:
                G, p, P, Q = witness
            elif len(witness) == 2:
                G, p = witness
                P = None
                Q = None
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # ¬Q: The intersection P \cap Q is not a strictly proper subgroup of N_P(P \cap Q) 
    # or not a strictly proper subgroup of N_Q(P \cap Q)
    try:
        # If P and Q are not explicitly provided, the counterexample to the false conjecture 
        # (which dropped the "distinct" hypothesis) is when P = Q.
        if P is None or Q is None:
            P = G.sylow_subgroup(p)
            Q = P

        P_elems = set(P.generate_dimino())
        Q_elems = set(Q.generate_dimino())
        int_elems = P_elems.intersection(Q_elems)

        # Calculate size of N_P(P \cap Q)
        norm_P_size = 0
        for g in P_elems:
            is_norm = True
            g_inv = ~g
            for h in int_elems:
                if g * h * g_inv not in int_elems:
                    is_norm = False
                    break
            if is_norm:
                norm_P_size += 1

        # Calculate size of N_Q(P \cap Q)
        norm_Q_size = 0
        for g in Q_elems:
            is_norm = True
            g_inv = ~g
            for h in int_elems:
                if g * h * g_inv not in int_elems:
                    is_norm = False
                    break
            if is_norm:
                norm_Q_size += 1

        int_size = len(int_elems)

        # The conclusion is that P \cap Q is strictly proper in both normalizers.
        # A subgroup is strictly proper if its size is strictly less than the parent group's size.
        # The negation is that it fails to be strictly proper in at least one of them.
        neg_q = not (int_size < norm_P_size and int_size < norm_Q_size)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: P \\cap Q is not a strictly proper subgroup of N_P(P \\cap Q) or not a strictly proper subgroup of N_Q(P \\cap Q)"
]

N_HYP = 2
NEG_Q_INDEX = 2