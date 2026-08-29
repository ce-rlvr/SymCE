import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        G, p, P, Q = witness
    except Exception:
        return [False, False, False]

    # H1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H2: P and Q are distinct Sylow p-subgroups of G
    try:
        def max_p_power(n, p):
            if p <= 1:
                return 1
            count = 0
            while n % p == 0:
                count += 1
                n //= p
            return p ** count

        def is_sylow(H, G, p):
            if not hasattr(H, 'generators') or not hasattr(H, 'order'):
                return False
            if not all(g in G for g in H.generators):
                return False
            if H.order() != max_p_power(G.order(), p):
                return False
            return True

        h2_ok = is_sylow(P, G, p) and is_sylow(Q, G, p)
        if h2_ok:
            # Check if they are distinct
            if P.order() == Q.order() and all(g in Q for g in P.generators):
                h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: P \cap Q is NOT a strictly proper subgroup of N_P(P \cap Q) 
    # OR P \cap Q is NOT a strictly proper subgroup of N_Q(P \cap Q)
    try:
        P_elems = set(P.generate())
        Q_elems = set(Q.generate())
        int_elems = list(P_elems.intersection(Q_elems))
        IntGroup = PermutationGroup(int_elems)
        
        int_order = IntGroup.order()
        
        def normalizer_order(Group, Subgroup):
            count = 0
            Subgroup_elems = set(Subgroup.generate())
            for g in Group.generate():
                if all((g * h * ~g) in Subgroup_elems for h in Subgroup.generators):
                    count += 1
            return count
        
        nP = normalizer_order(P, IntGroup)
        nQ = normalizer_order(Q, IntGroup)
        
        # A subgroup is strictly proper if its order is strictly less than the group's order.
        # The negation is that its order is greater than or equal to the normalizer's order.
        neg_q_ok = bool(int_order >= nP or int_order >= nQ)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P and Q are distinct Sylow p-subgroups of G",
    "¬Q: P \\cap Q is not a strictly proper subgroup of both N_P(P \\cap Q) and N_Q(P \\cap Q)"
]

N_HYP = 2
NEG_Q_INDEX = 2