import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import isprime

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a group G, or a tuple (G, p) where p is a prime.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        G, p = witness
    else:
        G = witness
        p = None

    # H_1: G is a non-abelian finite simple group
    try:
        h1 = False
        if hasattr(G, 'is_abelian') and not G.is_abelian:
            comp = G.composition_series()
            # A simple group has exactly 2 groups in its composition series: itself and the trivial group
            if len(comp) == 2:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The number of Sylow p-subgroups of G is NOT strictly greater than 1 (i.e., <= 1)
    try:
        neg_q = False
        if p is not None:
            if isprime(p):
                if G.order() % p != 0:
                    # If p does not divide |G|, the Sylow p-subgroup is trivial, so there is exactly 1.
                    n_p = 1
                else:
                    # Compute the number of Sylow p-subgroups by finding the orbit of one under conjugation
                    P = G.sylow_subgroup(p)
                    P_elements = frozenset(P.generate())
                    orbit = {P_elements}
                    queue = [P_elements]
                    gens = G.generators
                    
                    while queue:
                        curr = queue.pop(0)
                        for g in gens:
                            # Conjugate the subgroup elements by generator g
                            conj = frozenset(~g * x * g for x in curr)
                            if conj not in orbit:
                                orbit.add(conj)
                                queue.append(conj)
                    n_p = len(orbit)
                
                neg_q = (n_p <= 1)
        else:
            # If p is not provided, the conclusion "The number of Sylow p-subgroups of G is strictly greater than 1"
            # is interpreted as universally quantified over all primes p.
            # Since G is finite, there exists a prime p > G.order() such that n_p = 1.
            # Thus the universal conclusion fails, making its negation True.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian finite simple group",
    "¬Q: The number of Sylow p-subgroups of G is not strictly greater than 1"
]

N_HYP = 1
NEG_Q_INDEX = 1