import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: \phi and \psi are automorphisms of G",
    "H_3: \phi(s) = \psi(s) for all s \in S",
    "¬Q: \phi(x) != \psi(x) for some x \in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            S = witness.get('S')
            phi = witness.get('phi')
            psi = witness.get('psi')
        elif isinstance(witness, tuple) and len(witness) == 4:
            G, S, phi, psi = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def evaluate(f, x):
        if callable(f):
            return f(x)
        return f[x]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: \phi and \psi are automorphisms of G
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.generate())
            def is_auto(f):
                mapped = []
                for x in elements:
                    fx = evaluate(f, x)
                    if fx not in G:
                        return False
                    mapped.append(fx)
                # Check bijection
                if len(set(mapped)) != len(elements):
                    return False
                # Check homomorphism property
                for x in elements:
                    for y in elements:
                        if evaluate(f, x * y) != evaluate(f, x) * evaluate(f, y):
                            return False
                return True
            
            h2 = is_auto(phi) and is_auto(psi)
    except Exception:
        h2 = False

    # H_3: \phi(s) = \psi(s) for all s \in S
    try:
        if not h1:
            h3 = False
        else:
            h3 = True
            for s in S:
                if s not in G:
                    h3 = False
                    break
                if evaluate(phi, s) != evaluate(psi, s):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: \phi(x) != \psi(x) for some x \in G
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = False
            elements = list(G.generate())
            for x in elements:
                if evaluate(phi, x) != evaluate(psi, x):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]