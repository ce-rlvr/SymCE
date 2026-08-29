import sympy
import sympy.ntheory as nt
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: The number of distinct Sylow p-subgroups of G is exactly 1",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: p is a prime number
    try:
        h1_ok = bool(nt.isprime(p))
    except Exception:
        h1_ok = False

    # H2: P is a Sylow p-subgroup of G
    try:
        if not isinstance(p, (int, sympy.Integer)) or p <= 1:
            h2_ok = False
        else:
            order_G = G.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h2_ok = bool(P.is_subgroup(G) and P.order() == p**k)
    except Exception:
        h2_ok = False

    # H3: The number of distinct Sylow p-subgroups of G is exactly 1
    try:
        if not isinstance(p, (int, sympy.Integer)) or p <= 1:
            h3_ok = False
        else:
            true_sylow = G.sylow_subgroup(p)
            
            conjugates = []
            queue = [true_sylow]
            conjugates.append(true_sylow)
            gens = G.generators
            
            def is_in_conjugates(conj):
                for c in conjugates:
                    if c.is_subgroup(conj) and conj.is_subgroup(c):
                        return True
                return False

            while queue:
                current = queue.pop(0)
                for g in gens:
                    conj_gens = [g * x * ~g for x in current.generators]
                    if not conj_gens:
                        conj = current
                    else:
                        conj = PermutationGroup(conj_gens)
                    
                    if not is_in_conjugates(conj):
                        conjugates.append(conj)
                        queue.append(conj)
                        if len(conjugates) > 1:
                            break
                if len(conjugates) > 1:
                    break
            
            h3_ok = bool(len(conjugates) == 1)
    except Exception:
        h3_ok = False

    # neg_Q: P is not a normal subgroup of G
    try:
        neg_q_ok = not bool(G.is_normal(P))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]