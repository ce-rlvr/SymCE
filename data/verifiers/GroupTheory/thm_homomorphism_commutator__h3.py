import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, H, phi = witness
            x, y = None, None
        elif len(witness) == 5:
            G, H, phi, x, y = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    def is_group(grp):
        if type(grp).__name__ in ['PermutationGroup', 'FreeGroup', 'FpGroup']:
            return True
        if hasattr(grp, 'elements') or hasattr(grp, 'generate'):
            return True
        return False

    try:
        h1 = bool(is_group(G) and is_group(H))
    except Exception:
        h1 = False

    def check_homomorphism(G, H, phi):
        if type(phi).__name__ == 'Homomorphism':
            return True
        if isinstance(phi, dict):
            phi_func = lambda a: phi[a]
        elif callable(phi):
            phi_func = phi
        else:
            return False
            
        elements = []
        if hasattr(G, 'elements'):
            if isinstance(G.elements, (list, set, tuple)):
                elements = list(G.elements)
            else:
                for i, el in enumerate(G.elements):
                    if i > 100: break
                    elements.append(el)
        elif hasattr(G, 'generate'):
            for i, el in enumerate(G.generate()):
                if i > 100: break
                elements.append(el)
        else:
            return False
            
        for a in elements:
            for b in elements:
                if phi_func(a * b) != phi_func(a) * phi_func(b):
                    return False
        return True

    try:
        h2 = bool(check_homomorphism(G, H, phi))
    except Exception:
        h2 = False

    def check_neg_Q(G, H, phi, x, y):
        if type(phi).__name__ == 'Homomorphism':
            phi_func = phi
        elif isinstance(phi, dict):
            phi_func = lambda a: phi[a]
        elif callable(phi):
            phi_func = phi
        else:
            return False

        def comm(a, b):
            try:
                return a**-1 * b**-1 * a * b
            except Exception:
                return ~a * ~b * a * b

        if x is not None and y is not None:
            return bool(phi_func(comm(x, y)) != comm(phi_func(x), phi_func(y)))
        else:
            elements = []
            if hasattr(G, 'elements'):
                if isinstance(G.elements, (list, set, tuple)):
                    elements = list(G.elements)
                else:
                    for i, el in enumerate(G.elements):
                        if i > 50: break
                        elements.append(el)
            elif hasattr(G, 'generate'):
                for i, el in enumerate(G.generate()):
                    if i > 50: break
                    elements.append(el)
            
            for a in elements:
                for b in elements:
                    if phi_func(comm(a, b)) != comm(phi_func(a), phi_func(b)):
                        return True
            return False

    try:
        neg_q = bool(check_neg_Q(G, H, phi, x, y))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "not Q: phi(commutator(x, y)) != commutator(phi(x), phi(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2