import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.combinatorics.homomorphisms import homomorphism
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

def get_core(G, H):
    """Computes the core of H in G (the largest normal subgroup of G contained in H)."""
    core_elements = set(H.elements)
    for g in G.elements:
        ginv = ~g
        conj = {g * h * ginv for h in H.elements}
        core_elements = core_elements.intersection(conj)
        if len(core_elements) == 1:
            break
    return PermutationGroup(list(core_elements))

def is_normal_subgroup(G, K):
    """Checks if K is a normal subgroup of G."""
    try:
        K_elems = set(K.elements)
        if not K_elems.issubset(set(G.elements)):
            return False
        for g in G.generators:
            ginv = ~g
            for k in K.generators:
                if (g * k * ginv) not in K_elems:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # The witness should provide the group G, the subgroup H, and the missing action 
    # (or the kernel of the action, since the action itself was dropped from the hypotheses).
    try:
        if len(witness) == 3:
            G, H, action_or_kernel = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = isinstance(H, PermutationGroup) and set(H.elements).issubset(set(G.elements))
    except Exception:
        h2_ok = False

    # ¬Q: The kernel of the action is NOT the core of H
    try:
        if isinstance(action_or_kernel, PermutationGroup):
            kernel = action_or_kernel
            # If a subgroup is provided as the kernel, it must be a valid kernel of *some* action (i.e., normal in G)
            if not is_normal_subgroup(G, kernel):
                neg_q_ok = False
            else:
                core_H = get_core(G, H)
                neg_q_ok = set(kernel.elements) != set(core_H.elements)
        else:
            # Try to interpret the action as a homomorphism or a list/dict of generator images
            if hasattr(action_or_kernel, 'kernel'):
                kernel = action_or_kernel.kernel()
            elif isinstance(action_or_kernel, dict):
                img = PermutationGroup(list(action_or_kernel.values()))
                hom = homomorphism(G, img, action_or_kernel)
                kernel = hom.kernel()
            else:
                img = PermutationGroup(action_or_kernel)
                hom = homomorphism(G, img, G.generators, action_or_kernel)
                kernel = hom.kernel()
                
            core_H = get_core(G, H)
            neg_q_ok = set(kernel.elements) != set(core_H.elements)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The kernel of the action is not the core of H"
]

N_HYP = 2
NEG_Q_INDEX = 2