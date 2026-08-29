import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: x is an element of X, and G_x is the stabilizer of x in G",
    "¬Q: There is no bijection between the orbits of H on X and the double cosets H \\ G / G_x"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G = witness['G']
        x = witness['x']
        H = witness['H']
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group acting transitively on a set X.
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            h1 = G.is_transitive()
    except Exception:
        h1 = False

    # H_2: x is an element of X, and G_x is the stabilizer of x in G.
    try:
        if h1 and isinstance(x, int) and 0 <= x < G.degree:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The number of orbits of H on X is not equal to the number of double cosets H \ G / G_x.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if hasattr(H, 'generate'):
                H_elems = list(H.generate())
            else:
                H_elems = list(H)
            
            n = G.degree
            
            # Number of orbits of H on X
            orbits = set()
            for i in range(n):
                orbit = frozenset(h(i) for h in H_elems)
                if any(val >= n for val in orbit):
                    # H does not preserve X, so orbits on X are ill-defined
                    neg_q = False
                    break
                orbits.add(orbit)
            else:
                num_orbits = len(orbits)

                # Number of double cosets H \ G / G_x
                G_x = G.stabilizer(x)
                Gx_elems = list(G_x.generate())
                
                H_max_size = 0
                for h_elem in H_elems:
                    if hasattr(h_elem, 'size') and h_elem.size > H_max_size:
                        H_max_size = h_elem.size
                max_size = max(G.degree, H_max_size)
                
                def norm(p):
                    # Uniquely identify the permutation by its action on all points up to max_size
                    return tuple(p(i) for i in range(max_size))
                
                double_cosets = set()
                for g in G.generate():
                    # In SymPy, s * g * h applies s, then g, then h.
                    # This corresponds to the standard mathematical composition h(g(s(x))), i.e., the element hgs.
                    coset = frozenset(norm(s * g * h) for h in H_elems for s in Gx_elems)
                    double_cosets.add(coset)
                num_cosets = len(double_cosets)

                neg_q = (num_orbits != num_cosets)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]