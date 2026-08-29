import sympy
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
    try:
        # The witness is expected to be a group G
        if not isinstance(witness, PermutationGroup):
            return [False, False]
        
        # H_1: Inn(G) is the group of inner automorphisms of G.
        # This is a definitional hypothesis, which holds trivially for any valid group.
        h1_ok = True
        
        # Conclusion: The orbits of the action of Inn(G) on G are exactly the conjugacy classes of G.
        # We compute both the conjugacy classes and the orbits of Inn(G) on G.
        elements = list(witness.generate())
        
        conjugacy_classes = set()
        for x in elements:
            # Conjugacy class of x: {g * x * g^-1 | g in G}
            cclass = frozenset(g * x * ~g for g in elements)
            conjugacy_classes.add(cclass)
            
        orbits = set()
        for x in elements:
            # Inn(G) acts on G by inner automorphisms: phi_g(x) = g * x * g^-1
            # The orbit of x under this action is {phi_g(x) | g in G}
            orbit = frozenset(g * x * ~g for g in elements)
            orbits.add(orbit)
            
        conclusion = (orbits == conjugacy_classes)
        
        # The negated conclusion must be True when the conclusion FAILS at the witness
        neg_q_ok = not conclusion
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Inn(G) is the group of inner automorphisms of G",
    "¬Q: The orbits of the action of Inn(G) on G are not exactly the conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1