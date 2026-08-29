import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for the witness expression
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_distribution(G, x):
    """
    Computes the conjugacy class distribution of x.
    x can be a single element, a subset/list of elements, or a dict (group ring element).
    Returns a list of frequencies/coefficients for each conjugacy class.
    """
    if isinstance(x, dict):
        elements_dict = x
    elif hasattr(x, '__iter__') and not isinstance(x, Permutation):
        elements_dict = {}
        for e in x:
            elements_dict[e] = elements_dict.get(e, 0) + 1
    else:
        elements_dict = {x: 1}
        
    classes_elements = [list(C) for C in G.conjugacy_classes()]
    dist = [0] * len(classes_elements)
    
    for e, coeff in elements_dict.items():
        found = False
        for i, C_elems in enumerate(classes_elements):
            if e in C_elems:
                dist[i] += coeff
                found = True
                break
        if not found:
            return None  # Element not in G
    return dist

def are_conjugate(G, x, y):
    """
    Checks if x and y are conjugate in G.
    Supports elements, sets (subsets), lists (tuples), and dicts (group ring elements).
    """
    if isinstance(x, dict):
        if not isinstance(y, dict): return False
        for g in G.elements:
            conj_x = {}
            for e, coeff in x.items():
                ge_g = g * e * ~g
                conj_x[ge_g] = conj_x.get(ge_g, 0) + coeff
            if conj_x == y:
                return True
        return False
    elif isinstance(x, (set, frozenset)):
        if not isinstance(y, (set, frozenset)): return False
        set_y = set(y)
        for g in G.elements:
            conj_x = set(g * e * ~g for e in x)
            if conj_x == set_y:
                return True
        return False
    elif hasattr(x, '__iter__') and not isinstance(x, Permutation):
        list_y = list(y)
        for g in G.elements:
            conj_x = [g * e * ~g for e in x]
            if conj_x == list_y:
                return True
        return False
    else:
        for g in G.elements:
            if g * x * ~g == y:
                return True
        return False

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False, False]
        
    # H_1: Let G be a finite group.
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # Conclusion: x and y are conjugate in G if and only if chi(x) = chi(y) for every irreducible complex character chi of G.
    try:
        lhs = are_conjugate(G, x, y)
        
        dist_x = get_distribution(G, x)
        dist_y = get_distribution(G, y)
        
        if dist_x is None or dist_y is None:
            # If elements are not in G, characters are undefined, so the equivalence is invalid/false.
            conclusion = False
        else:
            # Characters are equal for all irreducible representations iff the conjugacy class distributions are identical.
            rhs = (dist_x == dist_y)
            conclusion = (lhs == rhs)
            
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The equivalence between conjugacy of x and y and equality of their characters fails"
]

N_HYP = 1
NEG_Q_INDEX = 1