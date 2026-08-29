import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - f: G -> H is a group homomorphism
      - A is a subgroup of G
    Conclusion:
      - f^{-1}(f(A)) = A ker(f)
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            A = witness['A']
        else:
            G, H, f, A = witness
            
        try:
            G_elements = list(G.elements)
        except AttributeError:
            G_elements = list(G)
            
        try:
            H_elements = list(H.elements)
        except AttributeError:
            H_elements = list(H)
            
        try:
            A_elements = list(A.elements)
        except AttributeError:
            A_elements = list(A)
            
        if callable(f):
            f_dict = {x: f(x) for x in G_elements}
        else:
            f_dict = f
            
        H_identity = None
        if hasattr(H, 'identity'):
            H_identity = H.identity
        else:
            for e in H_elements:
                if all(e * x == x and x * e == x for x in H_elements):
                    H_identity = e
                    break
    except Exception:
        return [False, False, False]

    # H_1: f: G -> H is a group homomorphism
    try:
        h1_ok = True
        for x in G_elements:
            if x not in f_dict:
                h1_ok = False
                break
            if f_dict[x] not in H_elements:
                h1_ok = False
                break
        if h1_ok:
            for x in G_elements:
                for y in G_elements:
                    if f_dict[x * y] != f_dict[x] * f_dict[y]:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: A is a subgroup of G
    try:
        A_set = set(A_elements)
        h2_ok = True
        if not A_set.issubset(set(G_elements)):
            h2_ok = False
        elif not A_set:
            h2_ok = False
        else:
            for x in A_set:
                if x**-1 not in A_set:
                    h2_ok = False
                    break
                for y in A_set:
                    if x * y not in A_set:
                        h2_ok = False
                        break
                if not h2_ok:
                    break
    except Exception:
        h2_ok = False

    # ¬Q: f^{-1}(f(A)) != A ker(f)
    try:
        if H_identity is None:
            neg_q = False
        else:
            A_set = set(A_elements)
            f_A = {f_dict[a] for a in A_set}
            preimage = {x for x in G_elements if f_dict.get(x) in f_A}
            ker_f = {x for x in G_elements if f_dict.get(x) == H_identity}
            A_ker_f = {a * k for a in A_set for k in ker_f}
            
            neg_q = preimage != A_ker_f
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: A is a subgroup of G",
    "¬Q: f^{-1}(f(A)) != A ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2