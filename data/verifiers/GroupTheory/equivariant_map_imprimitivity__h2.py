import itertools

# Top-level setup for standard objects
# (No specific named objects are strictly required for this domain, 
# but we provide standard group theory objects just in case the witness uses them)
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G = witness['G']
        X = witness['X']
        Y = witness['Y']
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        phi = witness['phi']
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting transitively on a set X
    try:
        h1 = True
        if not X:
            h1 = False
        else:
            perms = []
            for g in G:
                perm = {}
                for x in X:
                    perm[x] = action_X(g, x)
                # Action must be a bijection on X
                if len(set(perm.values())) != len(X):
                    h1 = False
                perms.append(perm)
            
            if h1:
                # Check identity exists
                has_id = False
                for p in perms:
                    if all(p[x] == x for x in X):
                        has_id = True
                        break
                if not has_id:
                    h1 = False
            
            if h1:
                # Check closure (which implies inverses for finite sets)
                for p1 in perms:
                    for p2 in perms:
                        comp = {x: p1[p2[x]] for x in X}
                        if comp not in perms:
                            h1 = False
                            break
                    if not h1:
                        break
            
            if h1:
                # Check transitivity
                orbit = set()
                x0 = X[0]
                for p in perms:
                    orbit.add(p[x0])
                if len(orbit) != len(X):
                    h1 = False
    except Exception:
        h1 = False

    # H_2: phi: X -> Y is a G-equivariant map
    try:
        h2 = True
        for g in G:
            for x in X:
                if phi(action_X(g, x)) != action_Y(g, phi(x)):
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # Conclusion: The set of non-empty fibers forms a system of imprimitivity.
    # A system of imprimitivity is typically defined as a non-trivial partition 
    # (i.e., not singletons and not the whole set) that is preserved by the group action.
    try:
        blocks = []
        phi_X = set(phi(x) for x in X)
        for y in phi_X:
            blocks.append(frozenset(x for x in X if phi(x) == y))
            
        is_system = True
        
        # 1. Check if the group action permutes the blocks (literal definition)
        for B in blocks:
            for g in G:
                gB = frozenset(action_X(g, x) for x in B)
                if gB not in blocks:
                    is_system = False
                    break
            if not is_system:
                break
                
        # 2. Check non-triviality (the dropped hypothesis was likely that phi is neither constant nor injective)
        if len(blocks) <= 1 or len(blocks) == len(X):
            is_system = False
            
        neg_q = not is_system
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: phi: X -> Y is a G-equivariant map",
    "¬Q: The set of non-empty fibers does NOT form a (non-trivial) system of imprimitivity for the action of G on X"
]

N_HYP = 2
NEG_Q_INDEX = 2