import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_orbit(group, pt):
    """
    Computes the orbit of a point under the action of a permutation group.
    Safely handles points outside the natural degree of the group.
    """
    orb = {pt}
    queue = [pt]
    while queue:
        curr = queue.pop(0)
        for gen in group.generators:
            # Permutations act as identity on points >= their size
            next_pt = gen(curr) if curr < gen.size else curr
            if next_pt not in orb:
                orb.add(next_pt)
                queue.append(next_pt)
    return orb

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple: (G, X, H, x)
        # where G is a PermutationGroup, X is a set/list of integers,
        # H is a PermutationGroup (subgroup of G), and x is an integer.
        G, X, H, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group acting transitively on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            X_set = set(X)
            if len(X_set) == 0:
                h1 = False
            else:
                x0 = list(X_set)[0]
                orbit_G = get_orbit(G, x0)
                h1 = (orbit_G == X_set)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if not isinstance(H, PermutationGroup):
            h2 = False
        else:
            # Check if all generators of H are elements of G
            h2 = all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # ¬Q: The number of orbits of H on X does NOT equal the number of double cosets H \ G / G_x
    try:
        X_set = set(X)
        
        # Compute the number of orbits of H on X
        orbits_H_X = set()
        for item in X_set:
            orbits_H_X.add(frozenset(get_orbit(H, item)))
        num_orbits_X = len(orbits_H_X)
        
        # Compute the number of double cosets H \ G / G_x
        # By standard group action theory, the double cosets H \ G / G_x are in bijection
        # with the orbits of H acting on the left cosets G / G_x.
        # Since G / G_x is G-equivariantly isomorphic to the orbit of x under G (G.x),
        # the number of double cosets equals the number of orbits of H on G.x.
        O_x = get_orbit(G, x)
        orbits_H_Ox = set()
        for y in O_x:
            orbits_H_Ox.add(frozenset(get_orbit(H, y)))
        num_double_cosets = len(orbits_H_Ox)
        
        neg_q = (num_orbits_X != num_double_cosets)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: H is a subgroup of G",
    "¬Q: The number of orbits of H on X does not equal the number of double cosets H \\ G / G_x"
]

N_HYP = 2
NEG_Q_INDEX = 2