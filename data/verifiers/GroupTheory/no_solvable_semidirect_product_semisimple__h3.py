import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def check_solvable(grp):
    """Helper to safely check if a SymPy group is solvable."""
    solv = grp.is_solvable
    if callable(solv):
        return solv()
    return solv

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    'If G is a semisimple finite group, N is a solvable group, and G is isomorphic 
    to the external semidirect product N \\rtimes H, then N is the trivial group.'
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H = witness.get('H')
        else:
            G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a semisimple finite group
    # A finite group is semisimple if it has no non-trivial solvable normal subgroups.
    try:
        h1 = True
        for K in G.normal_subgroups():
            if K.order() > 1 and check_solvable(K):
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: N is a solvable group
    try:
        h2 = bool(check_solvable(N))
    except Exception:
        h2 = False

    # H_3: G is isomorphic to the external semidirect product N \rtimes H
    try:
        h3 = False
        if G.order() == N.order() * H.order():
            normal_K = []
            for K in G.normal_subgroups():
                if K.order() == N.order() and K.is_isomorphic(N):
                    normal_K.append(('N', K))
                if K.order() == H.order() and K.is_isomorphic(H):
                    normal_K.append(('H', K))
            
            for role, K in normal_K:
                comp_order = H.order() if role == 'N' else N.order()
                comp_group = H if role == 'N' else N
                
                found_complement = False
                
                # 1. Fast path for prime order complements
                if isprime(comp_order):
                    for g in G.generate():
                        if g.order() == comp_order and not K.contains(g):
                            found_complement = True
                            break
                
                # 2. Fast path for cyclic complements
                if not found_complement:
                    is_comp_cyclic = any(x.order() == comp_order for x in comp_group.generate())
                    if is_comp_cyclic:
                        for g in G.generate():
                            if g.order() == comp_order:
                                intersect_trivial = True
                                for k in range(1, comp_order):
                                    if K.contains(g**k):
                                        intersect_trivial = False
                                        break
                                if intersect_trivial:
                                    found_complement = True
                                    break
                
                # 3. Fallback to full subgroup search if available
                if not found_complement:
                    try:
                        for C in G.subgroups():
                            if C.order() == comp_order and C.is_isomorphic(comp_group):
                                intersect_trivial = True
                                for g in C.generate():
                                    if getattr(g, 'is_Identity', False) or g.order() == 1:
                                        continue
                                    if K.contains(g):
                                        intersect_trivial = False
                                        break
                                if intersect_trivial:
                                    found_complement = True
                                    break
                    except AttributeError:
                        pass
                
                if found_complement:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: N is not the trivial group
    try:
        neg_q = bool(N.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: N is a solvable group",
    "H_3: G is isomorphic to the external semidirect product N \\rtimes H",
    "¬Q: N is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3