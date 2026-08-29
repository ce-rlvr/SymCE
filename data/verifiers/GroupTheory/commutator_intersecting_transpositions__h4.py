import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
            tau1 = witness.get('tau1')
            tau2 = witness.get('tau2')
            n = int(witness.get('n', 3))
            a = int(witness.get('a', 1))
            b = int(witness.get('b', 2))
            c = int(witness.get('c', 3))
        elif isinstance(witness, tuple) and len(witness) == 6:
            n, a, b, c, tau1, tau2 = witness
        else:
            perms = [x for x in witness if isinstance(x, Permutation)]
            if len(perms) >= 2:
                tau1, tau2 = perms[0], perms[1]
                supp = set(tau1.support()).union(tau2.support())
                n = max(supp) + 1 if supp else 3
                n = max(n, 3)
                a, b, c = 1, 2, 3
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = isinstance(n, int) and n >= 3
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(tau1, Permutation) and isinstance(tau2, Permutation)
        if h2_ok:
            supp1 = tau1.support()
            supp2 = tau2.support()
            max1 = max(supp1) if supp1 else -1
            max2 = max(supp2) if supp2 else -1
            if max1 >= n or max2 >= n:
                h2_ok = False
    except Exception:
        h2_ok = False

    try:
        h3_ok = (isinstance(a, int) and isinstance(b, int) and isinstance(c, int) and
                 len({a, b, c}) == 3 and
                 1 <= a <= n and 1 <= b <= n and 1 <= c <= n)
    except Exception:
        h3_ok = False

    try:
        comm = tau1 * tau2 * (~tau1) * (~tau2)
        cycles = comm.cyclic_form
        is_3_cycle = (len(cycles) == 1 and len(cycles[0]) == 3)
        neg_q_ok = not is_3_cycle
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: tau1 and tau2 are permutations in S_n",
    "H_3: a, b, c are three distinct elements from 1 to n",
    "¬Q: The commutator of tau1 and tau2 is not a 3-cycle"
]

N_HYP = 3
NEG_Q_INDEX = 3