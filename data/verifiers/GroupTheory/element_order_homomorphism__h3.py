import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            x = witness.get('x')
        else:
            G, H, f, x = witness
    except Exception:
        return [False, False, False]

    # H1: G and H are groups
    def is_group(grp):
        if grp is None: return False
        if getattr(grp, 'is_group', False):
            return True
        name = type(grp).__name__
        if name in ['PermutationGroup', 'FreeGroup', 'FpGroup', 'ProductGroup', 
                    'SymmetricGroup', 'CyclicGroup', 'AlternatingGroup', 'DihedralGroup']:
            return True
        if hasattr(grp, 'elements') or hasattr(grp, 'generators'):
            return True
        return False

    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    # H2: f is a group homomorphism
    def is_homomorphism(f, G, H):
        if f is None: return False
        if getattr(f, 'is_homomorphism', False):
            return True
        if callable(getattr(f, 'is_homomorphism', None)):
            return f.is_homomorphism()
        if type(f).__name__ == 'GroupHomomorphism':
            return True
            
        try:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
                for a, b in itertools.product(elements[:10], repeat=2):
                    ab = a * b
                    if isinstance(f, dict):
                        fa, fb, fab = f[a], f[b], f[ab]
                    else:
                        fa, fb, fab = f(a), f(b), f(ab)
                    if fab != fa * fb:
                        return False
                return True
            elif hasattr(G, 'generators'):
                gens = list(G.generators)
                for a, b in itertools.product(gens[:10], repeat=2):
                    ab = a * b
                    if isinstance(f, dict):
                        fa, fb, fab = f[a], f[b], f[ab]
                    else:
                        fa, fb, fab = f(a), f(b), f(ab)
                    if fab != fa * fb:
                        return False
                return True
        except Exception:
            pass
            
        if callable(f) or isinstance(f, dict):
            return True
            
        return False

    try:
        h2 = is_homomorphism(f, G, H)
    except Exception:
        h2 = False

    # neg_Q: The order of f(x) in H does NOT divide the order of x in G
    def get_order(elem, group):
        if hasattr(elem, 'order'):
            try:
                if callable(elem.order):
                    return elem.order()
                else:
                    return elem.order
            except Exception:
                pass
                
        if hasattr(elem, 'list') and hasattr(elem, 'size'):
            try:
                return elem.order()
            except Exception:
                pass
                
        try:
            if hasattr(group, 'identity'):
                e = group.identity
            else:
                e = elem ** 0
                
            curr = elem
            for i in range(1, 2000):
                if curr == e:
                    return i
                curr = curr * elem
        except Exception:
            pass
            
        return sympy.oo

    try:
        ord_x = get_order(x, G)
        
        if isinstance(f, dict):
            fx = f[x]
        else:
            fx = f(x)
            
        ord_fx = get_order(fx, H)
        
        if ord_x == sympy.oo or ord_x == float('inf'):
            neg_q = True
        elif ord_fx == sympy.oo or ord_fx == float('inf') or ord_fx == 0:
            neg_q = True
        else:
            neg_q = (ord_x % ord_fx != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: The order of f(x) in H does not divide the order of x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2