import math
import itertools
import functools
import sympy
from sympy.combinatorics import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            k = witness['k']
            n = witness['n']
            f = witness.get('f', None)
            f_provided = 'f' in witness
        else:
            if len(witness) == 3:
                G, k, n = witness
                f_provided = False
            elif len(witness) == 4:
                G, k, n, f = witness
                f_provided = True
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite cyclic group
    try:
        h1 = False
        if getattr(G, 'is_cyclic', False):
            if hasattr(G, 'order'):
                order = G.order()
                if order != sympy.oo:
                    h1 = True
        if not h1 and hasattr(G, 'elements') and hasattr(G, 'order'):
            order = G.order()
            if order != sympy.oo:
                order_int = int(order)
                elements = list(G.elements)
                for g in elements:
                    if int(g.order()) == order_int:
                        h1 = True
                        break
    except Exception:
        h1 = False

    # H2: k is an integer
    try:
        h2 = isinstance(k, int) or (hasattr(k, 'is_integer') and k.is_integer)
    except Exception:
        h2 = False

    # H3: f is the map defined by f(x) = x^k
    try:
        if f_provided:
            h3 = True
            elements = list(G.elements)
            for x in elements:
                if f(x) != x**k:
                    h3 = False
                    break
        else:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: f is a group automorphism of G iff gcd(k, n) = 1
    try:
        if not (isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer)):
            neg_q = False
        else:
            if f_provided:
                elements = list(G.elements)
                image = set()
                for x in elements:
                    image.add(f(x))
                is_auto = (len(image) == int(G.order()))
                is_homo = True
                for x in elements:
                    for y in elements:
                        if f(x * y) != f(x) * f(y):
                            is_homo = False
                            break
                    if not is_homo:
                        break
                is_auto = is_auto and is_homo
            else:
                is_auto = (math.gcd(int(k), int(G.order())) == 1)
                
            gcd_kn = math.gcd(int(k), int(n))
            conclusion = (is_auto == (gcd_kn == 1))
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: k is an integer",
    "H_3: f is the map defined by f(x) = x^k",
    "¬Q: f is a group automorphism of G iff gcd(k, n) = 1 is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3