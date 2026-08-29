import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Standard group bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)
# V4 (Klein four-group)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))

CONDITION_LABELS = [
    "H_1: G is a finite p-group for some prime p",
    "H_2: Phi(G) is the Frattini subgroup of G",
    "H_3: alpha is an automorphism of G",
    "H_4: The order of alpha is coprime to p",
    "¬Q: alpha is not the identity automorphism of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, alpha = witness
                Phi = None
            elif len(witness) == 3:
                G, Phi, alpha = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: G is a finite p-group for some prime p
    try:
        order = G.order()
        factors = sympy.ntheory.factorint(order)
        h1_ok = (len(factors) == 1)
        if h1_ok:
            p = list(factors.keys())[0]
    except Exception:
        h1_ok = False

    # H_2: Phi(G) is the Frattini subgroup of G
    try:
        if Phi is None:
            # If Phi is not explicitly provided in the witness, we consider the definition satisfied.
            h2_ok = True
        else:
            if h1_ok:
                elements = list(G.elements)
                gens = []
                # For a finite p-group, Phi(G) = G^p * [G, G]
                for g in elements:
                    gens.append(g**p)
                for g in elements:
                    for h in elements:
                        gens.append((g**-1) * (h**-1) * g * h)
                expected_Phi = PermutationGroup(gens)
                expected_elements = set(expected_Phi.elements)
                h2_ok = (set(Phi.elements) == expected_elements)
            else:
                h2_ok = False
    except Exception:
        h2_ok = False

    # H_3: alpha is an automorphism of G
    try:
        elements = list(G.elements)
        if isinstance(alpha, dict):
            alpha_dict = alpha
        elif callable(alpha):
            alpha_dict = {g: alpha(g) for g in elements}
        elif isinstance(alpha, list) and all(isinstance(item, tuple) and len(item) == 2 for item in alpha):
            alpha_dict = dict(alpha)
        else:
            alpha_dict = {}
            
        if len(alpha_dict) == len(elements):
            vals = set(alpha_dict.values())
            # Check bijection
            if len(vals) == len(elements) and all(g in alpha_dict and alpha_dict[g] in elements for g in elements):
                # Check homomorphism
                is_homo = True
                for g in elements:
                    for h in elements:
                        if alpha_dict[g * h] != alpha_dict[g] * alpha_dict[h]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                h3_ok = is_homo
            else:
                h3_ok = False
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # H_4: The order of alpha is coprime to p
    try:
        if h1_ok and h3_ok:
            current = {g: g for g in elements}
            k = 0
            while True:
                k += 1
                current = {g: alpha_dict[current[g]] for g in elements}
                if all(current[g] == g for g in elements):
                    break
                if k > 5000:  # Safety limit
                    k = 0
                    break
            if k > 0:
                h4_ok = (math.gcd(k, p) == 1)
            else:
                h4_ok = False
        else:
            h4_ok = False
    except Exception:
        h4_ok = False

    # ¬Q: alpha is not the identity automorphism of G
    try:
        if h3_ok:
            neg_q_ok = any(alpha_dict[g] != g for g in elements)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]