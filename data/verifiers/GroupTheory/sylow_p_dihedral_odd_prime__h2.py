import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import DihedralGroup, SymmetricGroup, AlternatingGroup, CyclicGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
        else:
            n, p = witness[:2]
            
        h1 = (int(n) == n) and (n >= 1)
        h2 = True
        
        if not (h1 and h2):
            return [False, False, False]
            
        if not isprime(p):
            return [bool(h1), bool(h2), False]
            
        n = int(n)
        if n >= 3:
            G = DihedralGroup(n)
        elif n == 2:
            G = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
        elif n == 1:
            G = PermutationGroup(Permutation(0, 1))
        else:
            return [bool(h1), bool(h2), False]
            
        S = G.sylow_subgroup(p)
        
        order = S.order()
        is_cyclic = False
        if order <= 3:
            is_cyclic = True
        else:
            for g in S.elements:
                if g.order() == order:
                    is_cyclic = True
                    break
                    
        is_normal = True
        for g in G.generators:
            g_inv = ~g
            for h in S.generators:
                conj = g * h * g_inv
                if conj not in S:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        neg_q = not (is_cyclic and is_normal)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the dihedral group of order 2n",
    "¬Q: Some Sylow p-subgroup of G is not cyclic or not normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2