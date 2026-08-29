import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        if hasattr(H, 'is_subgroup'):
            h1_ok = bool(H.is_subgroup(G))
        else:
            H_list = list(H)
            G_list = list(G)
            # Check subset
            h1_ok = all(any(h == g for g in G_list) for h in H_list)
            if h1_ok and len(H_list) > 0:
                # Check closure
                for a in H_list:
                    for b in H_list:
                        if not any(a * b == h for h in H_list):
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
                # Check identity and inverses
                if h1_ok:
                    has_id = False
                    for e in H_list:
                        if all(e * a == a and a * e == a for a in H_list):
                            has_id = True
                            for a in H_list:
                                has_inv = False
                                for b in H_list:
                                    if a * b == e and b * a == e:
                                        has_inv = True
                                        break
                                if not has_inv:
                                    h1_ok = False
                                    break
                            break
                    if not has_id:
                        h1_ok = False
            else:
                h1_ok = False
    except Exception:
        h1_ok = False
        
    try:
        if hasattr(G, 'generate'):
            g_elems = list(G.generate())
        else:
            g_elems = list(G)
            
        if hasattr(H, 'generate'):
            h_elems = list(H.generate())
        else:
            h_elems = list(H)
            
        def freeze(x):
            if hasattr(x, 'as_immutable'):
                return x.as_immutable()
            return x
            
        left_cosets = set()
        for g in g_elems:
            coset = frozenset([freeze(g * h) for h in h_elems])
            left_cosets.add(coset)
            
        right_cosets = set()
        for g in g_elems:
            coset = frozenset([freeze(h * g) for h in h_elems])
            right_cosets.add(coset)
            
        neg_q_ok = len(left_cosets) != len(right_cosets)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: There is no bijection between the set of left cosets and the set of right cosets of H in G"
]

N_HYP = 1
NEG_Q_INDEX = 1