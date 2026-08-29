import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    else:
        return list(G.generate())

def get_identity(G_elems):
    for g in G_elems:
        if getattr(g, 'is_Identity', False):
            return g
    return G_elems[0] * ~G_elems[0] if G_elems else Permutation()

def get_conjugacy_class_size(G, x):
    G_elems = get_elements(G)
    G_order = len(G_elems)
    id_elem = get_identity(G_elems)
    
    if isinstance(x, Permutation):
        C_gens = []
        for g in G_elems:
            if g * x * ~g == x:
                C_gens.append(g)
        C = PermutationGroup(C_gens) if C_gens else PermutationGroup([id_elem])
        return G_order // len(get_elements(C))
        
    elif isinstance(x, PermutationGroup):
        N_gens = []
        x_elems = set(get_elements(x))
        for g in G_elems:
            g_inv = ~g
            is_in_N = True
            for h in x.generators:
                if g * h * g_inv not in x_elems:
                    is_in_N = False
                    break
            if is_in_N:
                N_gens.append(g)
        N = PermutationGroup(N_gens) if N_gens else PermutationGroup([id_elem])
        return G_order // len(get_elements(N))
        
    elif isinstance(x, (list, set, tuple)):
        N_gens = []
        x_elems = set(x)
        for g in G_elems:
            g_inv = ~g
            conj_set = set(g * h * g_inv for h in x_elems)
            if conj_set == x_elems:
                N_gens.append(g)
        N = PermutationGroup(N_gens) if N_gens else PermutationGroup([id_elem])
        return G_order // len(get_elements(N))
        
    else:
        raise ValueError("Unknown type for x")

def get_centralizer(G, x):
    G_elems = get_elements(G)
    id_elem = get_identity(G_elems)
    
    if isinstance(x, Permutation):
        gens = []
        for g in G_elems:
            if g * x * ~g == x:
                gens.append(g)
        return PermutationGroup(gens) if gens else PermutationGroup([id_elem])
        
    elif isinstance(x, PermutationGroup):
        gens = []
        for g in G_elems:
            g_inv = ~g
            if all(g * h * g_inv == h for h in x.generators):
                gens.append(g)
        return PermutationGroup(gens) if gens else PermutationGroup([id_elem])
        
    elif isinstance(x, (list, set, tuple)):
        gens = []
        for g in G_elems:
            g_inv = ~g
            if all(g * h * g_inv == h for h in x):
                gens.append(g)
        return PermutationGroup(gens) if gens else PermutationGroup([id_elem])
        
    else:
        raise ValueError("Unknown type for x")

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    witness should be a tuple: (G, x, y)
    """
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The size of the conjugacy class of x and the size of the conjugacy class of y are relatively prime
    try:
        cx = get_conjugacy_class_size(G, x)
        cy = get_conjugacy_class_size(G, y)
        h2 = math.gcd(cx, cy) == 1
    except Exception:
        h2 = False

    # ¬Q: G does NOT factorize as the product of their centralizers (G != C_G(x) C_G(y))
    try:
        C_x = get_centralizer(G, x)
        C_y = get_centralizer(G, y)
        
        prod_set = set()
        for a in get_elements(C_x):
            for b in get_elements(C_y):
                prod_set.add(a * b)
        
        neg_q = len(prod_set) != len(get_elements(G))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The size of the conjugacy class of x and the size of the conjugacy class of y are relatively prime",
    "¬Q: G does not factorize as the product of their centralizers (G != C_G(x) C_G(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2