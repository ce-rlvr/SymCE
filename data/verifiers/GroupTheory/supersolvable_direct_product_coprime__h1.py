import math
import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z5 = CyclicGroup(5)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = math.gcd(int(G.order()), int(H.order())) == 1
    except Exception:
        h1 = False
        
    try:
        def is_supersolvable(grp):
            if int(grp.order()) == 1:
                return True
            normals = grp.normal_subgroups()
            normals = sorted(normals, key=lambda x: int(x.order()))
            
            def dfs(current_H):
                if int(current_H.order()) == int(grp.order()):
                    return True
                for next_H in normals:
                    if int(next_H.order()) > int(current_H.order()):
                        ratio = int(next_H.order()) // int(current_H.order())
                        if sympy.ntheory.isprime(ratio):
                            if all(next_H.contains(g) for g in current_H.generators):
                                if dfs(next_H):
                                    return True
                return False
            return dfs(normals[0])
            
        neg_q = not (is_supersolvable(G) and is_supersolvable(H))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The orders |G| and |H| are coprime",
    "¬Q: The direct product G x H is not supersolvable"
]

N_HYP = 1
NEG_Q_INDEX = 1