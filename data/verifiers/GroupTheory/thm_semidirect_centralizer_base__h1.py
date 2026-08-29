import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        # Extract G, N, H from the witness
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H = witness.get('H')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            G, N, H = witness
        else:
            G = getattr(witness, 'G', None)
            N = getattr(witness, 'N', None)
            H = getattr(witness, 'H', None)
            
        if G is None or N is None or H is None:
            return [False, False, False]
            
        # Verify they are valid groups
        if not (hasattr(G, 'is_group') and G.is_group): return [False, False, False]
        if not (hasattr(N, 'is_group') and N.is_group): return [False, False, False]
        if not (hasattr(H, 'is_group') and H.is_group): return [False, False, False]
        
        G_elems = set(G.elements)
        
        # Verify N and H are subgroups of G
        if not all(g in G_elems for g in N.generators): return [False, False, False]
        if not all(g in G_elems for g in H.generators): return [False, False, False]
        
        N_elems = set(N.elements)
        H_elems = set(H.elements)
        
        # Verify N is a normal subgroup of G
        is_normal = True
        for g in G.generators:
            for n in N.generators:
                if (g * n * ~g not in N_elems) or (~g * n * g not in N_elems):
                    is_normal = False
                    break
            if not is_normal:
                break
        if not is_normal: return [False, False, False]
        
        # Verify N and H intersect trivially
        if len(N_elems.intersection(H_elems)) != 1: return [False, False, False]
        
        # Verify G is the internal semidirect product of N and H
        if G.order() != N.order() * H.order(): return [False, False, False]
        
        # H_1: Z(N) is the center of the group N (definitional)
        h1 = True
        
        # H_2: C_G(N) is the centralizer of N in G (definitional)
        h2 = True
        
        # Compute centralizers and centers
        # An element commutes with all of N iff it commutes with the generators of N
        C_G_N = [g for g in G_elems if all(g * n == n * g for n in N.generators)]
        Z_N = [n for n in N_elems if all(n * m == m * n for m in N.generators)]
        
        # ker(phi) is the set of elements in H that act trivially on N (i.e., C_H(N))
        ker_phi = [h for h in H_elems if all(h * n == n * h for n in N.generators)]
        
        # The set of elements (n, h) corresponds to the products n * h
        Z_N_ker_phi = set(n * h for n in Z_N for h in ker_phi)
        
        # neg_Q: The conclusion fails if C_G(N) is not exactly the set of these products
        neg_q = set(C_G_N) != Z_N_ker_phi
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Z(N) is the center of the group N",
    "H_2: C_G(N) is the centralizer of N in G",
    "¬Q: C_G(N) is not given by the set of elements (n, h) where n in Z(N) and h in ker(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2