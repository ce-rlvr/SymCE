import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def center(G):
    Z = []
    G_elems = list(G.elements)
    for g in G_elems:
        if all(g * x == x * g for x in G_elems):
            Z.append(g)
    return Z

def centralizer(G, a):
    C = []
    for g in G.elements:
        if g * a == a * g:
            C.append(g)
    return C

def are_conjugate(G, a, b):
    for g in G.elements:
        if g * a * ~g == b:
            return True
    return False

def conditions(witness):
    try:
        G, A = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and hasattr(G, 'elements')
        if h1:
            order = G.order()
            h1 = order > 0
    except Exception:
        h1 = False
        
    # H2: A is a set of representatives for the distinct non-central conjugacy classes of G
    try:
        if not isinstance(A, (list, set, tuple)):
            h2 = False
        else:
            A_list = list(A)
            G_elems = list(G.elements)
            Z = center(G)
            
            h2 = True
            # All elements of A must be in G
            for a in A_list:
                if a not in G_elems:
                    h2 = False
                    break
            
            if h2:
                # No element of A is in Z(G)
                for a in A_list:
                    if a in Z:
                        h2 = False
                        break
            
            if h2:
                # Elements of A must be in distinct conjugacy classes
                for i in range(len(A_list)):
                    for j in range(i + 1, len(A_list)):
                        if are_conjugate(G, A_list[i], A_list[j]):
                            h2 = False
                            break
                    if not h2:
                        break
            
            if h2:
                # Every non-central element of G must be conjugate to some element of A
                for g in G_elems:
                    if g not in Z:
                        is_conj = False
                        for a in A_list:
                            if are_conjugate(G, g, a):
                                is_conj = True
                                break
                        if not is_conj:
                            h2 = False
                            break
    except Exception:
        h2 = False
        
    # Conclusion: |G| = |Z(G)| + \sum_{a \in A} [G : C_G(a)]
    try:
        G_elems = list(G.elements)
        Z = center(G)
        sum_index = 0
        A_list = list(A)
        for a in A_list:
            C = centralizer(G, a)
            sum_index += len(G_elems) // len(C)
            
        q = (len(G_elems) == len(Z) + sum_index)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: A is a set of representatives for the distinct non-central conjugacy classes of G",
    "neg_Q: Class equation fails"
]

N_HYP = 2
NEG_Q_INDEX = 2