import math
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, k = witness
                n = G.degree
            elif len(witness) == 3:
                G, k, n = witness
            else:
                return [False, False]
        else:
            return [False, False]
        k = int(k)
        n = int(n)
    except Exception:
        return [False, False]
        
    # H_1: G is a permutation group acting k-transitively on a set of size n
    h1_ok = False
    try:
        if isinstance(G, PermutationGroup):
            if n == G.degree:
                def check_trans(group, current_k, domain):
                    if current_k <= 0:
                        return True
                    if current_k > len(domain):
                        return True
                    if not domain:
                        return True
                    start = domain[0]
                    orbit = set([start])
                    queue = [start]
                    gens = group.generators
                    while queue:
                        curr = queue.pop(0)
                        for g in gens:
                            nxt = g(curr)
                            if nxt not in orbit:
                                orbit.add(nxt)
                                queue.append(nxt)
                    if len(orbit) != len(domain):
                        return False
                    if current_k == 1:
                        return True
                    stab = group.stabilizer(start)
                    new_domain = [x for x in domain if x != start]
                    return check_trans(stab, current_k - 1, new_domain)
                
                h1_ok = check_trans(G, k, list(range(n)))
    except Exception:
        h1_ok = False
        
    # neg_Q: The order of G is not divisible by n!/(n-k)!
    neg_q = False
    try:
        num = math.factorial(n)
        denom = math.factorial(n - k)
        if num % denom != 0:
            q_holds = False
        else:
            val = num // denom
            q_holds = (G.order() % val == 0)
    except Exception:
        # If factorial fails (e.g., negative argument when k > n), conclusion is undefined/fails
        q_holds = False
        
    neg_q = not q_holds
    
    return [h1_ok, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is a permutation group acting k-transitively on a set of size n",
    "¬Q: The order of G is not divisible by n!/(n-k)!"
]

N_HYP: int = 1
NEG_Q_INDEX: int = 1