import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
import math

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

def is_power_of_p(n, p):
    try:
        n = int(n)
        p = int(p)
        if n < 1:
            return False
        if n == 1:
            return True
        if p < 2:
            return False
        while n % p == 0:
            n //= p
        return n == 1
    except Exception:
        return False

def eval_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False] * 5
        G, H, f, p = witness
    except Exception:
        return [False] * 5

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f: G \to H is a group homomorphism
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            g_elements = list(G.generate())
            for x in g_elements:
                fx = eval_f(f, x)
                if fx not in H:
                    h2 = False
                    break
            if h2:
                for x in g_elements:
                    for y in g_elements:
                        fx = eval_f(f, x)
                        fy = eval_f(f, y)
                        fxy = eval_f(f, x * y)
                        if fxy != fx * fy:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(isprime(p))
    except Exception:
        h3 = False

    # H4: The image f(G) is a finite p-group
    try:
        if not (h1 and h3):
            h4 = False
        else:
            g_elements = list(G.generate())
            image_elements = set()
            for x in g_elements:
                fx = eval_f(f, x)
                image_elements.add(fx)
            img_size = len(image_elements)
            h4 = is_power_of_p(img_size, p)
    except Exception:
        h4 = False

    # neg_Q: G is not a finite p-group
    try:
        if not h1 or not h3:
            neg_q = False
        else:
            neg_q = not is_power_of_p(G.order(), p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "H_3: p is a prime number",
    "H_4: The image f(G) is a finite p-group",
    "¬Q: G is not a finite p-group"
]

N_HYP = 4
NEG_Q_INDEX = 4