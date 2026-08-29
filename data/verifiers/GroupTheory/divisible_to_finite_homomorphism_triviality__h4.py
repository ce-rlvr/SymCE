import sympy
from sympy import symbols, simplify, Lambda, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

# Dictionary of known infinite groups to support divisibility checks
# 'op' is the group operation, 'divisible' is a boolean, 'id' is the identity element
KNOWN_GROUPS = {
    'Q': {'op': '+', 'divisible': True, 'id': 0},
    'R': {'op': '+', 'divisible': True, 'id': 0},
    'C': {'op': '+', 'divisible': True, 'id': 0},
    'Z': {'op': '+', 'divisible': False, 'id': 0},
    'Q*': {'op': '*', 'divisible': False, 'id': 1},
    'R*': {'op': '*', 'divisible': False, 'id': 1},
    'C*': {'op': '*', 'divisible': True, 'id': 1},
    'R>0': {'op': '*', 'divisible': True, 'id': 1},
    'Q>0': {'op': '*', 'divisible': False, 'id': 1},
    sympy.S.Rationals: {'op': '+', 'divisible': True, 'id': 0},
    sympy.S.Reals: {'op': '+', 'divisible': True, 'id': 0},
    sympy.S.Complexes: {'op': '+', 'divisible': True, 'id': 0},
    sympy.S.Integers: {'op': '+', 'divisible': False, 'id': 0},
}

def is_known_group(G):
    try:
        return G in KNOWN_GROUPS
    except Exception:
        return False

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'G', 'H', and 'f', or a tuple (G, H, f).
    For infinite groups, use string names (e.g., 'Q', 'R*') or SymPy sets (e.g., sympy.S.Rationals).
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, H, f = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups
    try:
        G_is_group = is_known_group(G) or isinstance(G, PermutationGroup)
        H_is_group = is_known_group(H) or isinstance(H, PermutationGroup)
        h1 = bool(G_is_group and H_is_group)
    except Exception:
        h1 = False

    # H_2: f is a group homomorphism
    try:
        if not h1:
            h2 = False
        else:
            if is_known_group(G) and is_known_group(H):
                op_G = KNOWN_GROUPS[G]['op']
                op_H = KNOWN_GROUPS[H]['op']
                x, y = symbols('x y')
                
                g_xy = x + y if op_G == '+' else x * y
                
                if callable(f):
                    lhs = f(g_xy)
                    fx = f(x)
                    fy = f(y)
                elif isinstance(f, sympy.Expr):
                    syms = list(f.free_symbols)
                    var = syms[0] if syms else symbols('x')
                    lhs = f.subs(var, g_xy)
                    fx = f.subs(var, x)
                    fy = f.subs(var, y)
                else:
                    raise ValueError("f must be callable or a SymPy expression")
                
                rhs = fx + fy if op_H == '+' else fx * fy
                h2 = bool(simplify(lhs - rhs) == 0)
                
            elif isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                if type(f).__name__ == 'GroupHomomorphism':
                    h2 = bool(f.domain == G and f.codomain == H)
                elif callable(f):
                    h2 = True
                    for g1 in G.elements:
                        for g2 in G.elements:
                            if f(g1 * g2) != f(g1) * f(g2):
                                h2 = False
                                break
                elif isinstance(f, dict):
                    h2 = True
                    for g1 in G.elements:
                        for g2 in G.elements:
                            if f.get(g1 * g2) != f.get(g1) * f.get(g2):
                                h2 = False
                                break
                else:
                    h2 = False
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: G is a divisible group
    try:
        if not h1:
            h3 = False
        else:
            if is_known_group(G):
                h3 = bool(KNOWN_GROUPS[G]['divisible'])
            elif isinstance(G, PermutationGroup):
                # A finite group is divisible if and only if it is trivial
                h3 = bool(G.order() == 1)
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: The image of f is NOT the trivial subgroup of H
    try:
        if not h1:
            neg_q = False
        else:
            if is_known_group(G) and is_known_group(H):
                id_H = KNOWN_GROUPS[H]['id']
                x = symbols('x')
                
                if callable(f):
                    fx = f(x)
                elif isinstance(f, sympy.Expr):
                    syms = list(f.free_symbols)
                    var = syms[0] if syms else symbols('x')
                    fx = f.subs(var, x)
                else:
                    raise ValueError("f must be callable or a SymPy expression")
                
                is_trivial = bool(simplify(fx - id_H) == 0)
                neg_q = not is_trivial
                
            elif isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                id_H = H.identity
                if type(f).__name__ == 'GroupHomomorphism':
                    is_trivial = all(f(g) == id_H for g in G.elements)
                elif callable(f):
                    is_trivial = all(f(g) == id_H for g in G.elements)
                elif isinstance(f, dict):
                    is_trivial = all(f.get(g) == id_H for g in G.elements)
                else:
                    is_trivial = True
                neg_q = not is_trivial
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a group homomorphism",
    "H_3: G is a divisible group",
    "¬Q: The image of f is not the trivial subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3