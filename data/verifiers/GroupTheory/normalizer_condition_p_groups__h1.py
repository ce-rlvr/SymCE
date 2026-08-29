import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
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
    G, H = None, None
    p, n = None, None
    
    if isinstance(witness, tuple):
        if len(witness) >= 2:
            G, H = witness[0], witness[1]
        if len(witness) >= 3:
            p = witness[2]
        if len(witness) >= 4:
            n = witness[3]
    else:
        G = witness

    # H1: G is a finite group of order p^n for some integer n >= 1
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and G.order() < float('inf'):
            if p is not None and n is not None:
                try:
                    h1 = (G.order() == (int(p) ** int(n)) and int(n) >= 1)
                except Exception:
                    pass
            elif p is not None:
                try:
                    p_val = int(p)
                    order = G.order()
                    if order > 0 and p_val > 1:
                        temp = order
                        count = 0
                        while temp % p_val == 0 and temp > 1:
                            temp //= p_val
                            count += 1
                        if temp == 1 and count >= 1:
                            h1 = True
                    elif order == 1 and p_val == 1:
                        h1 = True
                except Exception:
                    pass
            else:
                if G.order() >= 2:
                    h1 = True
    except Exception:
        h1 = False

    # H2: H is a proper subgroup of G
    try:
        h2 = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            G_elements = set(G.generate())
            is_sub = True
            for h in H.generators:
                h_padded = h
                if hasattr(h, 'size') and hasattr(G, 'degree') and h.size != G.degree:
                    try:
                        h_padded = Permutation(h, size=G.degree)
                    except Exception:
                        pass
                if h_padded not in G_elements:
                    is_sub = False
                    break
            if is_sub and H.order() < G.order():
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: H is NOT strictly contained in its normalizer N_G(H)
    try:
        neg_q = False
        if h2:
            H_elements_padded = set()
            for h in H.generate():
                h_padded = h
                if hasattr(h, 'size') and hasattr(G, 'degree') and h.size != G.degree:
                    try:
                        h_padded = Permutation(h, size=G.degree)
                    except Exception:
                        pass
                H_elements_padded.add(h_padded)
            
            H_gens_padded = []
            for h in H.generators:
                h_padded = h
                if hasattr(h, 'size') and hasattr(G, 'degree') and h.size != G.degree:
                    try:
                        h_padded = Permutation(h, size=G.degree)
                    except Exception:
                        pass
                H_gens_padded.append(h_padded)

            strictly_contained = False
            for g in G.generate():
                if g in H_elements_padded:
                    continue
                
                normalizes = True
                for h in H_gens_padded:
                    if g * h * (~g) not in H_elements_padded:
                        normalizes = False
                        break
                
                if normalizes:
                    strictly_contained = True
                    break
            
            neg_q = not strictly_contained
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group of order p^n for some integer n >= 1",
    "H_2: H is a proper subgroup of G",
    "¬Q: H is not strictly contained in its normalizer N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2