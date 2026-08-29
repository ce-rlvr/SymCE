import sympy
import sympy.combinatorics as comb
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    G, p = None, None
    try:
        # Witness can be a tuple (Galois_group, prime_p) or just the Galois_group
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            # Attempt to infer p if only the group is provided
            if hasattr(G, 'order'):
                order = G.order()
                if order > 1:
                    factors = sympy.factorint(order)
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
    except Exception:
        pass

    # H_1: E is a finite Galois extension of F
    # Represented by the Galois group being a valid finite permutation group
    try:
        h1 = isinstance(G, comb.PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p) if p is not None else False
    except Exception:
        h2 = False

    # H_3: The Galois group Gal(E/F) is a p-group of order p^n for some integer n >= 1
    try:
        if p is not None:
            order = G.order()
            if order > 1:
                temp = order
                while temp % p == 0:
                    temp //= p
                h3 = (temp == 1)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: There does NOT exist an intermediate field K between F and E such that K/F is a Galois extension of degree p.
    # By Galois theory, K/F is Galois of degree p iff Gal(E/F) has a normal subgroup of index p.
    # A finite group G has a normal subgroup of index p iff its abelianization G/G' has order divisible by p.
    try:
        if p is not None and h1:
            G_prime = G.derived_subgroup()
            abelianization_order = G.order() // G_prime.order()
            has_normal_subgroup_index_p = (abelianization_order % p == 0)
            neg_q = not has_normal_subgroup_index_p
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E is a finite Galois extension of F",
    "H_2: p is a prime number",
    "H_3: The Galois group Gal(E/F) is a p-group of order p^n for some integer n >= 1",
    "¬Q: There does not exist an intermediate field K between F and E such that K/F is a Galois extension of degree p"
]

N_HYP = 3
NEG_Q_INDEX = 3