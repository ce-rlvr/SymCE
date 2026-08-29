import itertools
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_all_homomorphisms(G, H):
    """Finds all group homomorphisms from PermutationGroup G to PermutationGroup H."""
    G_elems = list(G.elements)
    H_elems = list(H.elements)
    
    id_G = None
    for e in G_elems:
        if e * e == e:
            id_G = e
            break
            
    id_H = None
    for e in H_elems:
        if e * e == e:
            id_H = e
            break

    gens = G.generators
    homomorphisms = []
    
    for target in itertools.product(H_elems, repeat=len(gens)):
        phi = {id_G: id_H}
        queue = [id_G]
        valid = True
        
        for g, t in zip(gens, target):
            if g in phi:
                if phi[g] != t:
                    valid = False
                    break
            else:
                phi[g] = t
                queue.append(g)
                
        if not valid:
            continue
            
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                val = phi[curr] * phi[g]
                if nxt in phi:
                    if phi[nxt] != val:
                        valid = False
                        break
                else:
                    phi[nxt] = val
                    queue.append(nxt)
            if not valid:
                break
                
        if valid and len(phi) == len(G_elems):
            is_homo = True
            for x in G_elems:
                for y in G_elems:
                    if phi[x*y] != phi[x]*phi[y]:
                        is_homo = False
                        break
                if not is_homo:
                    break
            if is_homo:
                homomorphisms.append(phi)
                
    return homomorphisms

def conditions(witness) -> list[bool]:
    # H_1: Let H be a group.
    try:
        H = witness['H']
        h1 = isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Let f: X -> H be a mapping.
    try:
        X = witness['X']
        f = witness['f']
        H_elems = list(H.elements)
        if isinstance(f, dict):
            h2 = all(x in f and f[x] in H_elems for x in X)
        elif callable(f):
            h2 = True
            for x in X:
                try:
                    if f(x) not in H_elems:
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: For every relation w=1 in R, the substitution of f(x) for each x in X 
    # in the word w yields the identity element in H.
    try:
        R = witness['R']
        h3 = True
        id_H = None
        for e in H.elements:
            if e * e == e:
                id_H = e
                break
                
        for w in R:
            val = id_H
            for x in w:
                fx = f[x] if isinstance(f, dict) else f(x)
                val = val * fx
            if val != id_H:
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: It is NOT the case that there exists a unique group homomorphism phi: G -> H 
    # such that phi(x) = f(x) for all x in X.
    try:
        G = witness['G']
        if not isinstance(G, PermutationGroup):
            neg_q = True
        else:
            homomorphisms = get_all_homomorphisms(G, H)
            valid_homos = []
            for phi in homomorphisms:
                try:
                    match = True
                    for x in X:
                        fx = f[x] if isinstance(f, dict) else f(x)
                        if phi[x] != fx:
                            match = False
                            break
                    if match:
                        valid_homos.append(phi)
                except KeyError:
                    # If x is not in phi, it means x is not in G, so phi doesn't extend f on X
                    pass
            
            # The conclusion fails if there is no such homomorphism, or more than one.
            neg_q = len(valid_homos) != 1
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: f is a mapping from X to H",
    "H_3: For every relation w=1 in R, substituting f(x) yields the identity in H",
    "¬Q: There does not exist a unique group homomorphism phi: G -> H extending f"
]

N_HYP = 3
NEG_Q_INDEX = 3