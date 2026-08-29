import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        else:
            G, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(G, PermutationGroup)
    except Exception:
        h2_ok = False

    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            S = []
            for x in G.elements:
                order = x.order()
                temp = order
                if temp < 1:
                    is_power = False
                else:
                    while temp > 1 and temp % p == 0:
                        temp = temp // p
                    is_power = (temp == 1)
                
                if is_power:
                    S.append(x)
            
            S_set = set(S)
            is_subgroup = True
            for x in S:
                for y in S:
                    if (x * y) not in S_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            
            neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a group",
    "¬Q: S is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2