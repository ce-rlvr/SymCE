import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        G = witness['G']
        X = witness['X']
        action = witness['action']
        x = witness['x']
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a set
    try:
        h2 = isinstance(X, (set, frozenset, list, tuple)) or hasattr(X, 'is_FiniteSet')
        X_list = list(X)
    except Exception:
        h2 = False

    # H_3: G acts on X
    try:
        h3 = True
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
        else:
            G_elements = list(G.generate())
            
        id_G = G.identity
        
        # 1. Identity acts trivially
        for y in X_list:
            if action(id_G, y) != y:
                h3 = False
                break
                
        # 2. Closure of action on X
        if h3:
            for g in G_elements:
                for y in X_list:
                    if action(g, y) not in X_list:
                        h3 = False
                        break
                if not h3: break
                
        # 3. Compatibility (left action axiom)
        if h3:
            for g in G_elements:
                for h in G_elements:
                    for y in X_list:
                        if action(g, action(h, y)) != action(g * h, y):
                            h3 = False
                            break
                    if not h3: break
                if not h3: break
    except Exception:
        h3 = False

    # ¬Q: The map g*Stab_G(x) |-> g.x is not a well-defined bijection between G/Stab_G(x) and Orb_G(x)
    try:
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
        else:
            G_elements = list(G.generate())
            
        # Compute the stabilizer of x
        stab = [g for g in G_elements if action(g, x) == x]
        
        # Check if Stab_G(x) is a valid subgroup
        is_subgroup = True
        if G.identity not in stab:
            is_subgroup = False
        else:
            for s1 in stab:
                for s2 in stab:
                    if s1 * s2 not in stab:
                        is_subgroup = False
                        break
                if not is_subgroup: break
            if is_subgroup:
                for s in stab:
                    if s**-1 not in stab:
                        is_subgroup = False
                        break
                        
        if not is_subgroup:
            # If the stabilizer is not a subgroup, the set of left cosets is not well-defined
            neg_q = True
        else:
            # Compute left cosets
            cosets = {}
            for g in G_elements:
                coset = frozenset([g * s for s in stab])
                cosets[g] = coset
                
            # Check if the map is well-defined
            well_defined = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if cosets[g1] == cosets[g2]:
                        if action(g1, x) != action(g2, x):
                            well_defined = False
                            break
                if not well_defined: break
                
            # Check if the map is injective
            injective = True
            if well_defined:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if action(g1, x) == action(g2, x):
                            if cosets[g1] != cosets[g2]:
                                injective = False
                                break
                    if not injective: break
                    
            # Surjectivity is guaranteed by definition of the orbit.
            # The conclusion fails if the map is not well-defined or not injective.
            neg_q = not (well_defined and injective)
    except Exception:
        # If evaluating the action on x raises an error, the map is not well-defined
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "¬Q: The map g*Stab_G(x) |-> g.x is not a well-defined bijection between G/Stab_G(x) and Orb_G(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3