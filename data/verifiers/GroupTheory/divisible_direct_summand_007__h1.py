import sympy
from sympy.combinatorics import SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup
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
    Checks if the witness is a valid counterexample.
    
    The witness should be an object representing a group G and a subgroup H,
    with the following attributes and methods:
      - G_elements: list of representative elements of G (must include elements outside H if H != G)
      - H_elements: list of representative elements of H (must include non-identity elements)
      - op(a, b): returns the group operation a * b
      - inv(a): returns the inverse of a
      - eq(a, b): returns True if a and b represent the same group element
      - in_H(a): returns True if a is in H
      - divide_H(h, n): returns an element x in H such that x^n = h
      
    Example counterexample: G = Q ⋊ Z_2, H = Q.
    """
    try:
        G_elems = witness.G_elements
        H_elems = witness.H_elements
        
        # H_1: H is a divisible subgroup of G
        h_subgroup = True
        if not H_elems:
            h_subgroup = False
        for h1 in H_elems:
            if not witness.in_H(h1):
                h_subgroup = False
            if not witness.in_H(witness.inv(h1)):
                h_subgroup = False
            for h2 in H_elems:
                if not witness.in_H(witness.op(h1, h2)):
                    h_subgroup = False
                    
        h_divisible = True
        for h in H_elems:
            for n in range(1, 11): # Check divisibility for n=1 to 10
                x = witness.divide_H(h, n)
                if not witness.in_H(x):
                    h_divisible = False
                    break
                # compute x^n
                curr = x
                for _ in range(n - 1):
                    curr = witness.op(curr, x)
                if not witness.eq(curr, h):
                    h_divisible = False
                    break
            if not h_divisible:
                break
                
        h1_ok = h_subgroup and h_divisible
        
        # neg_Q: H is NOT a direct summand of G
        # Sufficient condition: H is a proper subgroup, and C_G(H) <= H.
        # If C_G(H) <= H, any subgroup K commuting with H must be contained in H.
        # Since a direct summand K must have H \cap K = {e}, K must be {e}.
        # Then HK = H != G, so G is not H \oplus K.
        h_proper = False
        for g in G_elems:
            if not witness.in_H(g):
                h_proper = True
                break
                
        cg_in_h = True
        for g in G_elems:
            if witness.in_H(g):
                continue
            # g is not in H. Check if it commutes with all h in H_elems
            commutes_with_all = True
            for h in H_elems:
                gh = witness.op(g, h)
                hg = witness.op(h, g)
                if not witness.eq(gh, hg):
                    commutes_with_all = False
                    break
            if commutes_with_all:
                # Found an element outside H that commutes with all H_elems
                # So C_G(H) is not contained in H (at least for the tested elements)
                cg_in_h = False
                break
                
        neg_q = h_proper and cg_in_h
        
        return [bool(h1_ok), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: H is a divisible subgroup of G",
    "¬Q: H is not a direct summand of G"
]

N_HYP = 1
NEG_Q_INDEX = 1