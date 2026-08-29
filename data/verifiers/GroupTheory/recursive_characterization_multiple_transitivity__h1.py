import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide a set of permutations G, a domain Omega, and an integer k.
    """
    try:
        if isinstance(witness, dict):
            G_set = witness['G']
            Omega = witness['Omega']
            k = witness['k']
        elif isinstance(witness, tuple) and len(witness) == 3:
            G_set, Omega, k = witness
        else:
            G_set = witness.G
            Omega = witness.Omega
            k = witness.k
    except Exception:
        return [False, False, False]

    # H_1: k is an integer strictly greater than 1
    try:
        h1_ok = isinstance(k, int) and k > 1
    except Exception:
        h1_ok = False

    # H_2: The cardinality of \Omega is at least k
    try:
        Omega_list = []
        for x in Omega:
            if x not in Omega_list:
                Omega_list.append(x)
        h2_ok = len(Omega_list) >= k
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion fails at the witness.
    # Conclusion: G is k-transitive iff (G is transitive AND for all alpha, G_alpha is (k-1)-transitive)
    try:
        G_list = list(G_set)

        def apply_g(g, x):
            try: return g(x)
            except Exception: pass
            try: return g ^ x
            except Exception: pass
            try: return g[x]
            except Exception: pass
            return x

        def is_k_trans(G, dom, k_val):
            if k_val == 0:
                return True
            for tup1 in itertools.permutations(dom, k_val):
                for tup2 in itertools.permutations(dom, k_val):
                    found = False
                    for g in G:
                        if all(apply_g(g, x) == y for x, y in zip(tup1, tup2)):
                            found = True
                            break
                    if not found:
                        return False
            return True

        # P: G is k-transitive on \Omega
        P = is_k_trans(G_list, Omega_list, k)

        # Q: G is transitive on \Omega AND for any \alpha \in \Omega, G_\alpha acts (k-1)-transitively on \Omega \setminus \{\alpha\}
        Q_part1 = is_k_trans(G_list, Omega_list, 1)
        Q_part2 = True
        if Q_part1:
            for alpha in Omega_list:
                G_alpha = [g for g in G_list if apply_g(g, alpha) == alpha]
                dom_minus_alpha = [x for x in Omega_list if x != alpha]
                if not is_k_trans(G_alpha, dom_minus_alpha, k - 1):
                    Q_part2 = False
                    break
        Q = Q_part1 and Q_part2

        # The conjecture claims P == Q. It fails if P != Q.
        neg_q_ok = (P != Q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is an integer strictly greater than 1",
    "H_2: The cardinality of \\Omega is at least k",
    "¬Q: G is k-transitive on \\Omega is NOT equivalent to (G is transitive and G_alpha acts (k-1)-transitively)"
]

N_HYP = 2
NEG_Q_INDEX = 2
