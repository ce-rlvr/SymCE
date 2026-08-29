import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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
    Given a witness tuple (G, p, phi, P) or a dictionary with these keys,
    checks the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            p = witness['p']
            phi = witness['phi']
            P = witness['P']
        else:
            G, p, phi, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
        # Limit group size to prevent timeouts during evaluation
        if h1 and G.order() > 2000:
            h1 = False
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h2 = False

    # H_3: \phi is an automorphism of G
    try:
        if not h1:
            h3 = False
        else:
            elements = list(G.generate())
            if isinstance(phi, dict):
                mapping = phi
            else:
                mapping = {g: phi(g) for g in elements}
            
            h3 = True
            # Check bijection
            if set(mapping.keys()) != set(elements):
                h3 = False
            elif set(mapping.values()) != set(elements):
                h3 = False
            else:
                # Check homomorphism property
                for g in elements:
                    for h in elements:
                        if mapping[g * h] != mapping[g] * mapping[h]:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # ¬Q: The image \phi(P) is NOT a Sylow p-subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            if hasattr(P, 'generate'):
                P_elements = set(P.generate())
            else:
                P_elements = set(P)
                
            if isinstance(phi, dict):
                phi_P = {phi[g] for g in P_elements}
            else:
                phi_P = {phi(g) for g in P_elements}
                
            p_val = int(p)
            order_G = G.order()
            k = 0
            if p_val > 1:
                while order_G % (p_val**(k+1)) == 0:
                    k += 1
            expected_order = p_val**k
            
            is_sylow = True
            if len(phi_P) != expected_order:
                is_sylow = False
            elif not phi_P.issubset(set(G.generate())):
                is_sylow = False
            else:
                identity = G.identity
                if identity not in phi_P:
                    is_sylow = False
                else:
                    # Check closure under group operation
                    for x in phi_P:
                        for y in phi_P:
                            if x * y not in phi_P:
                                is_sylow = False
                                break
                        if not is_sylow:
                            break
            
            neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: \\phi is an automorphism of G",
    "¬Q: The image \\phi(P) is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3