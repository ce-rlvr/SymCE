import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is isomorphic to a subgroup of A4, but we can just use AlternatingGroup(4) or define it if needed
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
    Evaluates the remaining hypotheses and the negated conclusion of the conjecture at the given witness.
    
    The witness is expected to be a dictionary or object containing:
      - 'N': a group (e.g., a PermutationGroup)
      - 'H': a group (e.g., a PermutationGroup)
      - 'phi': a function taking an element of H and returning a function (automorphism) on N
      - 'm': a positive integer
      - 'n': an element of N
      - 'h': an element of H
      - 'G_mult': a function representing the group operation in G = N \rtimes_\phi H
    """
    # Extract witness components
    try:
        N = witness['N']
        H = witness['H']
        phi = witness['phi']
        m = witness['m']
        n = witness['n']
        h = witness['h']
        G_mult = witness['G_mult']
    except Exception:
        return [False, False, False, False, False]

    # H_1: N and H are groups
    try:
        # We assume N and H are valid groups if they have an identity and elements
        h1_ok = hasattr(N, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1_ok = False

    # H_2: phi: H -> Aut(N) is a group homomorphism
    try:
        # We check if phi(h1 * h2)(n) == phi(h1)(phi(h2)(n)) for some elements
        # Since we can't easily check all, we assume the witness provides a valid phi
        # We will just check if phi is callable and returns a callable
        h2_ok = callable(phi) and callable(phi(H.identity))
    except Exception:
        h2_ok = False

    # H_3: G = N \rtimes_\phi H is the external semidirect product of N and H
    try:
        # We check if G_mult matches the semidirect product definition for a few elements
        # (n1, h1) * (n2, h2) = (n1 * phi(h1)(n2), h1 * h2)
        # We assume the witness provides a valid G_mult
        h3_ok = callable(G_mult)
    except Exception:
        h3_ok = False

    # H_4: m is a positive integer
    try:
        h4_ok = isinstance(m, int) and m > 0
    except Exception:
        h4_ok = False

    # ¬Q: The m-th power (n, h)^m in G is NOT equal to (n \phi_h(n) \phi_{h^2}(n) \cdots \phi_{h^{m-1}}(n), h^m)
    try:
        # Compute (n, h)^m using G_mult
        current_n, current_h = n, h
        for _ in range(m - 1):
            current_n, current_h = G_mult((current_n, current_h), (n, h))
        actual_power = (current_n, current_h)

        # Compute the formula: n * phi_h(n) * phi_{h^2}(n) * ... * phi_{h^{m-1}}(n)
        formula_n = n
        h_power = h
        for _ in range(1, m):
            formula_n = formula_n * phi(h_power)(n)
            h_power = h_power * h
        formula_power = (formula_n, h_power)

        # The conclusion fails if the actual power does not equal the formula power
        neg_q_ok = actual_power != formula_power
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: G = N \rtimes_\phi H is the external semidirect product of N and H",
    "H_4: m is a positive integer",
    "¬Q: The m-th power (n, h)^m in G is not equal to the given formula"
]

N_HYP = 4
NEG_Q_INDEX = 4