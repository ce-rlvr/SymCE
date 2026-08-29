import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    # H_1: G and H are groups
    try:
        G = witness['G']
        H = witness['H']
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1 = False

    # H_2: f: G -> H is a group homomorphism
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        
        if isinstance(f, dict):
            f_map = lambda g: f[g]
        elif isinstance(f, (list, tuple)):
            f_dict = dict(f)
            f_map = lambda g: f_dict[g]
        else:
            f_map = f
            
        h2 = True
        H_elements = list(H.elements)
        for g in G.elements:
            if f_map(g) not in H_elements:
                h2 = False
                break
                
        if h2:
            for g1 in G.elements:
                for g2 in G.elements:
                    if f_map(g1 * g2) != f_map(g1) * f_map(g2):
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H_3: x and y are elements of G such that x and y are conjugate in G
    try:
        G = witness['G']
        x = witness['x']
        y = witness['y']
        
        h3 = False
        G_elements = list(G.elements)
        if x in G_elements and y in G_elements:
            for g in G_elements:
                if y == ~g * x * g or y == g * x * ~g:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: f(x) != f(y)
    try:
        f = witness['f']
        x = witness['x']
        y = witness['y']
        
        if isinstance(f, dict):
            f_map = lambda g: f[g]
        elif isinstance(f, (list, tuple)):
            f_dict = dict(f)
            f_map = lambda g: f_dict[g]
        else:
            f_map = f
            
        neg_q = f_map(x) != f_map(y)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a group homomorphism",
    "H_3: x and y are elements of G such that x and y are conjugate in G",
    "¬Q: f(x) != f(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3