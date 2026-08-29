import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should provide G, X, action, x, and H.
    """
    if isinstance(witness, dict):
        G = witness.get('G')
        X = witness.get('X')
        action = witness.get('action')
        x = witness.get('x')
        H = witness.get('H')
    elif isinstance(witness, (tuple, list)) and len(witness) >= 5:
        G, X, action, x, H = witness[:5]
    else:
        return [False] * 5

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple)) and len(X) > 0
    except Exception:
        h2 = False

    # H3: G acts transitively on X
    try:
        if not (h1 and h2):
            h3 = False
        else:
            G_elements = list(G)
            
            # Find the identity element safely
            id_elem = None
            for g in G_elements:
                is_id = True
                for h_elem in G_elements:
                    if g * h_elem != h_elem:
                        is_id = False
                        break
                if is_id:
                    id_elem = g
                    break
            
            valid_action = True
            if id_elem is not None:
                for y in X:
                    if action(id_elem, y) != y:
                        valid_action = False
                        break
            else:
                valid_action = False

            if valid_action:
                for g in G_elements:
                    for h_elem in G_elements:
                        for y in X:
                            if action(g, action(h_elem, y)) != action(g * h_elem, y):
                                valid_action = False
                                break
                        if not valid_action:
                            break
                    if not valid_action:
                        break
            
            if valid_action:
                transitive = True
                for y in X:
                    orbit_y = []
                    for g in G_elements:
                        orbit_y.append(action(g, y))
                    for z in X:
                        if z not in orbit_y:
                            transitive = False
                            break
                    if not transitive:
                        break
                h3 = transitive
            else:
                h3 = False
    except Exception:
        h3 = False

    # H4: x \in X
    try:
        h4 = x in X
    except Exception:
        h4 = False

    # neg_Q: Conclusion fails
    # The conclusion is that \phi(gH) = g \cdot x is a well-defined G-set isomorphism from G/H to X.
    # This holds if and only if H is exactly the stabilizer of x.
    try:
        if not (h1 and h2 and h4) or H is None:
            neg_q = False
        else:
            G_elements = list(G)
            if not isinstance(H, PermutationGroup):
                neg_q = True
            else:
                H_elements = list(H)
                is_subgroup = all(h_elem in G_elements for h_elem in H_elements)
                if not is_subgroup:
                    neg_q = True
                else:
                    stabilizer = []
                    for g in G_elements:
                        if action(g, x) == x:
                            stabilizer.append(g)
                    
                    stab_set = set(stabilizer)
                    h_set = set(H_elements)
                    
                    if stab_set == h_set:
                        neg_q = False  # Conclusion holds
                    else:
                        neg_q = True   # Conclusion fails
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "H_4: x in X",
    "¬Q: The map phi(gH) = g * x is not a well-defined G-set isomorphism from G/H to X"
]

N_HYP = 4
NEG_Q_INDEX = 4