import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: A is a set of representatives for the distinct non-central conjugacy classes of G",
    "¬Q: |G| != |Z(G)| + sum_{a in A} (G : C_G(a))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, Z, A = witness
        else:
            G = witness
            Z = G.center()
            classes = G.conjugacy_classes()
            A = [c[0] for c in classes if len(c) > 1]
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(G, 'center'):
            C = G.center()
            if hasattr(C, 'elements'):
                C_elems = set(C.elements)
            else:
                C_elems = set(C)
                
            if hasattr(Z, 'elements'):
                Z_elems = set(Z.elements)
            else:
                Z_elems = set(Z)
                
            h1 = (Z_elems == C_elems)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(G, 'conjugacy_classes'):
            classes = G.conjugacy_classes()
            non_central = [set(c) for c in classes if len(c) > 1]
            A_elems = set(A)
            if len(A_elems) != len(non_central):
                h2 = False
            else:
                h2 = all(len(A_elems.intersection(c)) == 1 for c in non_central)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if hasattr(G, 'order'):
            G_order = G.order()
        else:
            G_order = len(G)
            
        if hasattr(Z, 'order'):
            Z_order = Z.order()
        else:
            Z_order = len(Z)
            
        sum_index = 0
        for a in A:
            index = None
            if hasattr(G, 'centralizer'):
                try:
                    H = PermutationGroup([a])
                    C_a = G.centralizer(H)
                    C_a_order = C_a.order()
                    if G_order == sympy.oo:
                        index = sympy.oo
                    else:
                        index = G_order // C_a_order
                except Exception:
                    pass
                if index is None:
                    try:
                        C_a = G.centralizer(a)
                        C_a_order = C_a.order() if hasattr(C_a, 'order') else len(C_a)
                        if G_order == sympy.oo:
                            index = sympy.oo
                        else:
                            index = G_order // C_a_order
                    except Exception:
                        pass
            
            if index is None and hasattr(G, 'conjugacy_classes'):
                for c in G.conjugacy_classes():
                    if a in c:
                        index = len(c)
                        break
                        
            if index is None:
                raise ValueError("Cannot compute index")
                
            sum_index += index
            
        q = (G_order == Z_order + sum_index)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]