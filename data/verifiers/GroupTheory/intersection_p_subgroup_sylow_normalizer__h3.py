import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint, isprime

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
    def check_h1():
        try:
            G, p, H, P = witness
            if not isinstance(G, PermutationGroup): return False
            if not isinstance(P, PermutationGroup): return False
            G_elts = set(G.generate())
            if not all(g in G_elts for g in P.generators): return False
            return True
        except Exception:
            return False

    def check_h2():
        try:
            G, p, H, P = witness
            return bool(isprime(p))
        except Exception:
            return False

    def check_h3():
        try:
            G, p, H, P = witness
            if not isinstance(H, PermutationGroup): return False
            G_elts = set(G.generate())
            if not all(g in G_elts for g in H.generators): return False
            
            order = H.order()
            if order == 1:
                return True
            factors = factorint(order)
            return list(factors.keys()) == [p]
        except Exception:
            return False

    def check_neg_q():
        try:
            G, p, H, P = witness
            H_elts = set(H.generate())
            P_elts = set(P.generate())
            
            N_G_P_elts = set()
            for g in G.generate():
                is_norm = True
                for p_gen in P.generators:
                    if (g * p_gen * (~g)) not in P_elts:
                        is_norm = False
                        break
                if is_norm:
                    N_G_P_elts.add(g)
                    
            left = H_elts.intersection(N_G_P_elts)
            right = H_elts.intersection(P_elts)
            
            return left != right
        except Exception:
            return False

    return [check_h1(), check_h2(), check_h3(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: G is a finite group and P is a subgroup of G",
    "H_2: p is a prime number",
    "H_3: H is a p-subgroup of G",
    "¬Q: H \\cap N_G(P) \\neq H \\cap P"
]

N_HYP = 3
NEG_Q_INDEX = 3