import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def perm_eq(p1, p2):
    """Check equality of permutations, ignoring trailing fixed points."""
    try:
        if hasattr(p1, 'array_form') and hasattr(p2, 'array_form'):
            a1 = list(p1.array_form)
            a2 = list(p2.array_form)
            while a1 and a1[-1] == len(a1) - 1: a1.pop()
            while a2 and a2[-1] == len(a2) - 1: a2.pop()
            return a1 == a2
    except Exception:
        pass
    return p1 == p2

def in_elems(x, elems):
    return any(perm_eq(x, e) for e in elems)

def get_inv(x):
    try:
        return x**-1
    except Exception:
        return ~x

def conditions(witness) -> list[bool]:
    try:
        G, H, a = witness
    except Exception:
        return [False, False, False, False]
        
    def get_elements(group):
        if hasattr(group, 'elements'):
            return list(group.elements)
        return list(group)
        
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = len(G_elems) > 0 and all(in_elems(x * y, G_elems) for x in G_elems for y in G_elems)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(in_elems(h, G_elems) for h in H_elems)
        else:
            h2 = (len(H_elems) > 0 and 
                  all(in_elems(h, G_elems) for h in H_elems) and 
                  all(in_elems(x * y, H_elems) for x in H_elems for y in H_elems))
    except Exception:
        h2 = False

    # H_3: G acts on the set of left cosets G/H by left multiplication
    try:
        # This is a mathematical tautology for any valid group and subgroup
        h3 = h1 and h2
    except Exception:
        h3 = False

    # ¬Q: The stabilizer of the coset aH under this action is not the conjugate subgroup aHa^{-1}
    try:
        a_inv = get_inv(a)
        
        # The stabilizer of aH in G is {g \in G | a^{-1} g a \in H}
        stab = []
        for g in G_elems:
            if in_elems(a_inv * g * a, H_elems):
                stab.append(g)
                
        # The conjugate subgroup is aHa^{-1}
        aha = []
        for h in H_elems:
            aha.append(a * h * a_inv)
            
        # Check if stab and aha contain exactly the same elements
        stab_is_aha = (len(stab) == len(aha)) and all(in_elems(x, aha) for x in stab) and all(in_elems(x, stab) for x in aha)
        neg_q = not stab_is_aha
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: G acts on the set of left cosets G/H by left multiplication",
    "¬Q: The stabilizer of the coset aH under this action is not the conjugate subgroup aHa^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3