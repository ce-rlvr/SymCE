import sympy
from sympy import S
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard group theory and linear algebra objects
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

# Infinite group Z (integers under addition) for counterexamples
class Z_Group:
    def __init__(self):
        self.identity = 0
        # A symmetric sample around the identity to test properties
        self.sample = list(range(-100, 101))
        
    def op(self, a, b):
        return a + b
        
    def inv(self, a):
        return -a

Z = Z_Group()
Z_group = Z

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, phi, f = witness
        elif len(witness) == 2:
            G, phi = witness
            f = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if G == S.Integers:
            sample = [S(i) for i in range(-100, 101)]
            identity = S(0)
            op = lambda a, b: a + b
            inv = lambda a: -a
        elif hasattr(G, 'sample'):
            sample = G.sample
            identity = G.identity
            op = G.op
            inv = G.inv
        else:
            sample = list(G.elements)
            identity = G.identity
            op = lambda a, b: a * b
            inv = lambda a: a**-1
            
        if f is None:
            f = lambda x: op(inv(x), phi(x))
            
    except Exception:
        return [False, False, False, False]

    # H1: phi is an automorphism of G
    try:
        h1_ok = True
        phi_image = []
        sample_set = set(sample)
        
        for a in sample:
            pa = phi(a)
            phi_image.append(pa)
            for b in sample:
                ab = op(a, b)
                # Only check homomorphism if the result is within our sample bounds
                if ab in sample_set:
                    if phi(ab) != op(pa, phi(b)):
                        h1_ok = False
                        break
            if not h1_ok:
                break
                
        if h1_ok:
            # Bijection check on the sample
            phi_image_set = set(phi_image)
            if len(phi_image_set) != len(sample_set):
                h1_ok = False
            else:
                for x in sample_set:
                    if x not in phi_image_set:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H2: For all g \in G, \phi(g) = g implies g = e
    try:
        h2_ok = True
        for g in sample:
            if phi(g) == g:
                if g != identity:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # H3: f(x) = x^{-1} \phi(x)
    try:
        h3_ok = True
        for g in sample:
            expected = op(inv(g), phi(g))
            if f(g) != expected:
                h3_ok = False
                break
    except Exception:
        h3_ok = False

    # Negated Conclusion: f is NOT a bijection
    try:
        f_image = []
        is_injective = True
        seen = set()
        for g in sample:
            fg = f(g)
            f_image.append(fg)
            if fg in seen:
                is_injective = False
            seen.add(fg)
        
        f_image_set = set(f_image)
        is_surjective = True
        for y in sample_set:
            if y not in f_image_set:
                is_surjective = False
                break
                
        neg_q_ok = not (is_injective and is_surjective)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is an automorphism of G",
    "H_2: For all g in G, phi(g) = g implies g = e",
    "H_3: f: G -> G is defined by f(x) = x^{-1}phi(x)",
    "¬Q: The map f is not a bijection"
]

N_HYP = 3
NEG_Q_INDEX = 3