import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            S = witness.get('S')
        else:
            G, p, S = witness
    except Exception:
        return [False, False, False]

    # H_1: G is an abelian group
    try:
        h1 = bool(G.is_abelian)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # ¬Q: S is not a subgroup of G
    try:
        def check_subgroup(G, S):
            try:
                if hasattr(S, 'is_subgroup'):
                    try:
                        return bool(S.is_subgroup(G))
                    except Exception:
                        pass
                
                try:
                    S_list = list(S)
                except Exception:
                    return False
                    
                if not S_list:
                    return False
                    
                for x in S_list:
                    if x not in G:
                        return False
                        
                for x in S_list:
                    for y in S_list:
                        if x * y not in S_list:
                            return False
                            
                for x in S_list:
                    if x**-1 not in S_list:
                        return False
                        
                return True
            except Exception:
                return False

        neg_q = not check_subgroup(G, S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: p is a prime number",
    "¬Q: S is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2