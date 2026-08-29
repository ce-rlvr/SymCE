import math
import sympy
from sympy.combinatorics import (
    PermutationGroup, SymmetricGroup, AlternatingGroup,
    DihedralGroup, CyclicGroup, Permutation
)
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
            f_provided = 'f' in witness
            if f_provided:
                f = witness['f']
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, k = witness
                f_provided = False
            elif len(witness) == 3:
                G, f, k = witness
                f_provided = True
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a finite abelian group
    try:
        h1 = hasattr(G, 'is_abelian') and bool(G.is_abelian)
        order = G.order()
        h1 = h1 and (order > 0) and (order < float('inf'))
    except Exception:
        h1 = False

    # H2: f is the map defined by f(x) = x^k for all x in G
    try:
        h2 = isinstance(k, (int, sympy.Integer))
        if f_provided:
            elements = list(G.elements)
            h2 = h2 and all(f(x) == x**int(k) for x in elements)
    except Exception:
        h2 = False

    # neg_Q: The equivalence (f is an automorphism of G if and only if gcd(k, |G|) = 1) fails
    try:
        elements = list(G.elements)
        
        # Check if f is a homomorphism
        is_hom = True
        for x in elements:
            for y in elements:
                if (x * y)**int(k) != (x**int(k)) * (y**int(k)):
                    is_hom = False
                    break
            if not is_hom:
                break
        
        # Check if f is a bijection (surjectivity implies bijection for finite sets)
        image = []
        for x in elements:
            val = x**int(k)
            if val not in image:
                image.append(val)
        is_bij = len(image) == len(elements)
        
        is_auto = is_hom and is_bij
        
        gcd_cond = math.gcd(int(k), int(G.order())) == 1
        
        # The conclusion is the biconditional: is_auto <-> gcd_cond
        # The negation is that they have different truth values
        neg_q = (is_auto != gcd_cond)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: f is the map defined by f(x) = x^k for all x in G",
    "¬Q: The equivalence (f is an automorphism iff gcd(k, |G|) = 1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2