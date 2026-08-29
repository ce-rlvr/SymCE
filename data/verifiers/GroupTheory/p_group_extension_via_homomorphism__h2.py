import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

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
        G = witness['G']
        H = witness['H']
        p = witness['p']
        f = witness['f']
    except Exception:
        return [False, False, False, False, False]

    def is_power_of_p(n, p):
        try:
            n = int(n)
            p = int(p)
        except Exception:
            return False
        if n <= 0 or p <= 1: 
            return False
        if n == 1: 
            return True
        while n % p == 0:
            n //= p
        return n == 1

    def get_identity(group):
        for e in group.elements:
            if e * e == e:
                return e
        return None

    def is_subgroup(elements, group):
        if not elements:
            return False
        identity = get_identity(group)
        if identity not in elements:
            return False
        for a in elements:
            for b in elements:
                if a * b not in elements:
                    return False
        return True

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: The kernel of f is a finite p-group
    try:
        if isinstance(f, dict):
            eval_f = lambda x: f[x]
        else:
            eval_f = f
            
        H_identity = get_identity(H)
        ker_f = set()
        for x in G.elements:
            if eval_f(x) == H_identity:
                ker_f.add(x)
        h3 = bool(is_subgroup(ker_f, G) and is_power_of_p(len(ker_f), p))
    except Exception:
        h3 = False

    # H4: The image f(G) is a finite p-group
    try:
        if isinstance(f, dict):
            eval_f = lambda x: f[x]
        else:
            eval_f = f
            
        im_f = set()
        for x in G.elements:
            im_f.add(eval_f(x))
        h4 = bool(is_subgroup(im_f, H) and is_power_of_p(len(im_f), p))
    except Exception:
        h4 = False

    # neg_Q: G is not a finite p-group
    try:
        neg_q = not is_power_of_p(G.order(), p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: p is a prime number",
    "H_3: The kernel of f is a finite p-group",
    "H_4: The image f(G) is a finite p-group",
    "¬Q: G is not a finite p-group"
]

N_HYP = 4
NEG_Q_INDEX = 4