import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            phi = witness.get('phi')
            Z = witness.get('Z', None)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, Z, phi = witness
            elif len(witness) == 2:
                G, phi = witness
                Z = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if G is None or phi is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def evaluate_phi(f, x):
        if isinstance(f, dict):
            return f[x]
        elif isinstance(f, Permutation):
            return f * x * (~f)
        elif isinstance(f, list):
            for k, v in f:
                if k == x:
                    return v
            raise ValueError("Mapping not found")
        else:
            return f(x)

    # H_1: G is a non-abelian group
    try:
        h1 = hasattr(G, 'elements') and (not G.is_abelian)
    except Exception:
        h1 = False

    # H_2: Z(G) is the center of G
    try:
        if Z is not None:
            center_elements = set(G.center().elements)
            z_elements = set(Z.elements)
            h2 = (center_elements == z_elements)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H_3: \phi is an automorphism of G
    try:
        elements = list(G.elements)
        mapped_elements = []
        h3 = True
        for g in elements:
            val = evaluate_phi(phi, g)
            if val not in elements:
                h3 = False
                break
            mapped_elements.append(val)
        
        if h3:
            if len(set(mapped_elements)) != len(elements):
                h3 = False
            else:
                for g in elements:
                    for h in elements:
                        val_g = evaluate_phi(phi, g)
                        val_h = evaluate_phi(phi, h)
                        val_gh = evaluate_phi(phi, g * h)
                        if val_gh != val_g * val_h:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # ¬Q: \phi is not the identity automorphism on G
    try:
        neg_q = False
        elements = list(G.elements)
        for g in elements:
            val = evaluate_phi(phi, g)
            if val != g:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "H_2: Z(G) is the center of G",
    "H_3: \\phi is an automorphism of G",
    "¬Q: \\phi is not the identity automorphism on G"
]

N_HYP = 3
NEG_Q_INDEX = 3