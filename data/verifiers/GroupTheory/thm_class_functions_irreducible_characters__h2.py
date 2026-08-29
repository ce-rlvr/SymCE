import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def get_val(f, g):
    if isinstance(f, dict):
        return f[g]
    else:
        return f(g)

def is_complex_constant(v):
    if isinstance(v, (int, float, complex)):
        return True
    if hasattr(v, 'free_symbols') and len(v.free_symbols) > 0:
        return False
    if hasattr(v, 'is_complex'):
        if v.is_complex is False:
            return False
    try:
        complex(v)
        return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, f = witness
            elif len(witness) == 3:
                G, Irr, f = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Irr(G) is the set of all irreducible complex characters of G
    # We verify this definitional hypothesis by ensuring f is well-defined on all elements of G
    try:
        h2 = False
        if h1:
            for g in G.elements:
                _ = get_val(f, g)
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The equivalence fails (f is a class function XOR f can be expressed as a linear combination of characters over C)
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            is_class_func = True
            classes = G.conjugacy_classes()
            for c in classes:
                elements = list(c)
                if not elements:
                    continue
                val0 = get_val(f, elements[0])
                for g in elements[1:]:
                    if get_val(f, g) != val0:
                        is_class_func = False
                        break
                if not is_class_func:
                    break
            
            all_complex = True
            for g in G.elements:
                if not is_complex_constant(get_val(f, g)):
                    all_complex = False
                    break
            
            lhs = is_class_func
            # Since the irreducible characters form a basis for the space of complex-valued class functions,
            # f can be expressed as a linear combination of complex characters over C iff it is a complex-valued class function.
            rhs = is_class_func and all_complex
            
            neg_q = not (lhs == rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Irr(G) is the set of all irreducible complex characters of G",
    "¬Q: f is constant on each conjugacy class of G XOR f can be expressed as a linear combination of the characters in Irr(G) over \\mathbb{C}"
]

N_HYP = 2
NEG_Q_INDEX = 2