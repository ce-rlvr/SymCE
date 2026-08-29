import sympy
from sympy.combinatorics import PermutationGroup, Permutation, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def safe_prop(obj, prop):
    """Safely evaluate a property that might be a method or an attribute."""
    val = getattr(obj, prop)
    return val() if callable(val) else val

def wreath_product(A, B):
    """Constructs the wreath product A wr B for permutation groups A and B."""
    d = A.degree
    n = B.degree
    gens = []
    
    # Generators for the base group A^n
    for i in range(n):
        for g in A.generators:
            perm = list(range(d * n))
            for j in range(d):
                perm[i * d + j] = i * d + g(j)
            gens.append(Permutation(perm))
            
    # Generators for the top group B
    for g in B.generators:
        perm = list(range(d * n))
        for i in range(n):
            for j in range(d):
                perm[g(i) * d + j] = i * d + j
        gens.append(Permutation(perm))
        
    if not gens:
        gens.append(Permutation(max(0, d * n - 1)))
        
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    # H1: S is a finite non-abelian simple group
    try:
        S = witness.S
        is_simple = safe_prop(S, 'is_simple')
        is_abelian = safe_prop(S, 'is_abelian')
        order = safe_prop(S, 'order')
        h1 = bool(is_simple) and not bool(is_abelian) and order < float('inf')
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        n = witness.n
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # neg_Q: Aut(G) is NOT isomorphic to Aut(S) wr S_n
    try:
        G = witness.G
        S = witness.S
        n = witness.n
        
        # If the witness explicitly provides the automorphism groups, check isomorphism rigorously
        if hasattr(witness, 'AutG') and hasattr(witness, 'AutS'):
            AutS = witness.AutS
            AutG = witness.AutG
            Sn = SymmetricGroup(n)
            wr = wreath_product(AutS, Sn)
            neg_q = not AutG.is_isomorphic(wr)
        else:
            # Fallback heuristic: if AutG is not provided, we check if G is isomorphic to S^n.
            # If it is not, we assume Aut(G) is not isomorphic to Aut(S) wr S_n.
            Sn_group = DirectProduct(*[S]*n)
            neg_q = not G.is_isomorphic(Sn_group)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a finite non-abelian simple group",
    "H_2: n is a positive integer",
    "¬Q: Aut(G) is not isomorphic to Aut(S) wr S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2