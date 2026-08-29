import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            S = witness.get('S')
            phi = witness.get('phi')
            psi = witness.get('psi')
        else:
            G, S, phi, psi = witness
    except Exception:
        return [False, False, False, False]

    def evaluate_map(f, x):
        if isinstance(f, (dict, list, tuple)):
            return f[x]
        else:
            return f(x)

    def get_elements(G):
        if hasattr(G, 'elements'):
            return list(G.elements)
        elif hasattr(G, 'generate'):
            return list(G.generate())
        else:
            return list(G)

    try:
        elements = get_elements(G)
    except Exception:
        return [False, False, False, False]

    # H1: S is a generating set for G
    try:
        if not S:
            h1 = (len(elements) == 1)
        else:
            if not all(s in elements for s in S):
                h1 = False
            else:
                subgroup = []
                for s in S:
                    if s not in subgroup:
                        subgroup.append(s)
                queue = list(subgroup)
                while queue:
                    x = queue.pop(0)
                    for s in S:
                        xs = x * s
                        if xs not in subgroup:
                            subgroup.append(xs)
                            queue.append(xs)
                h1 = (len(subgroup) == len(elements))
    except Exception:
        h1 = False

    # H2: \phi and \psi are automorphisms of G
    def is_automorphism(f):
        try:
            mapped = []
            for x in elements:
                fx = evaluate_map(f, x)
                if fx not in elements:
                    return False
                if fx not in mapped:
                    mapped.append(fx)
            if len(mapped) != len(elements):
                return False
            for x in elements:
                fx = evaluate_map(f, x)
                for y in elements:
                    fy = evaluate_map(f, y)
                    fxy = evaluate_map(f, x * y)
                    if fxy != fx * fy:
                        return False
            return True
        except Exception:
            return False

    try:
        h2 = is_automorphism(phi) and is_automorphism(psi)
    except Exception:
        h2 = False

    # H3: \phi(s) = \psi(s) for all s \in S
    try:
        h3 = all(evaluate_map(phi, s) == evaluate_map(psi, s) for s in S)
    except Exception:
        h3 = False

    # neg_Q: \phi(x) != \psi(x) for some x \in G
    try:
        neg_q = any(evaluate_map(phi, x) != evaluate_map(psi, x) for x in elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a generating set for G",
    "H_2: phi and psi are automorphisms of G",
    "H_3: phi(s) == psi(s) for all s in S",
    "¬Q: phi(x) != psi(x) for some x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3