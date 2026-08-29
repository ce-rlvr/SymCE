import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(sub, grp):
    try:
        if not hasattr(sub, 'generators'):
            return False
        for g in sub.generators:
            if g not in grp:
                return False
        return True
    except Exception:
        return False

def is_hall_subgroup(sub, grp):
    try:
        if not is_subgroup(sub, grp):
            return False
        o_sub = sub.order()
        o_grp = grp.order()
        if o_grp % o_sub != 0:
            return False
        return math.gcd(o_sub, o_grp // o_sub) == 1
    except Exception:
        return False

def are_conjugate(G, H, K):
    try:
        if H.order() != K.order():
            return False
        gens_H = H.generators
        try:
            elements = list(G.generate_dimino())
        except AttributeError:
            elements = list(G.elements)
            
        for g in elements:
            is_conj = True
            for h in gens_H:
                if (g * h * g**-1) not in K:
                    is_conj = False
                    break
            if is_conj:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            G, H, K = witness[:3]
        elif isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            K = witness.get('K')
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: Let G be a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H_2: G is a solvable group
    try:
        h2 = bool(G.is_solvable)
    except Exception:
        h2 = False
        
    # H_3: Let H and K be Hall \pi-subgroups of G
    # (In the context of the dropped hypothesis, they are independent Hall subgroups)
    try:
        h3 = is_hall_subgroup(H, G) and is_hall_subgroup(K, G)
    except Exception:
        h3 = False
        
    # neg_Q: H and K are NOT conjugate subgroups in G
    try:
        neg_q = not are_conjugate(G, H, K)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a solvable group",
    "H_3: H and K are Hall pi-subgroups of G",
    "not Q: H and K are not conjugate subgroups in G"
]

N_HYP = 3
NEG_Q_INDEX = 3