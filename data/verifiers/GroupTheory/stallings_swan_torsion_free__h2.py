import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Setup standard groups
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
    # H_1: G is a finitely generated group
    try:
        t_name = type(witness).__name__
        h1 = t_name in ('FpGroup', 'FreeGroup', 'PermutationGroup') or isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is torsion-free
    try:
        t_name = type(witness).__name__
        if t_name == 'FreeGroup':
            h2 = True
        elif isinstance(witness, PermutationGroup):
            h2 = witness.order() == 1
        elif t_name == 'FpGroup':
            invs = witness.abelian_invariants()
            if any(i != 0 for i in invs):
                h2 = False
            else:
                F = witness.free_group
                gens = F.generators
                n = len(gens)
                expected_comms = set()
                for i in range(n):
                    for j in range(i+1, n):
                        g1, g2 = gens[i], gens[j]
                        expected_comms.add(g1*g2*g1**-1*g2**-1)
                        expected_comms.add(g2*g1*g2**-1*g1**-1)
                        expected_comms.add(g1**-1*g2**-1*g1*g2)
                        expected_comms.add(g2**-1*g1**-1*g2*g1)
                        expected_comms.add(g1*g2**-1*g1**-1*g2)
                        expected_comms.add(g2*g1**-1*g2**-1*g1)
                        expected_comms.add(g1**-1*g2*g1*g2**-1)
                        expected_comms.add(g2**-1*g1*g2*g1**-1)
                
                if len(witness.relators) > 0 and all(r in expected_comms for r in witness.relators):
                    h2 = True
                elif len(witness.relators) == 0:
                    h2 = True
                else:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G is not a free group
    try:
        t_name = type(witness).__name__
        if t_name == 'FreeGroup':
            is_free = True
        elif isinstance(witness, PermutationGroup):
            is_free = witness.order() == 1
        elif t_name == 'FpGroup':
            invs = witness.abelian_invariants()
            if any(i != 0 for i in invs):
                is_free = False
            else:
                k = len(invs)
                g = len(witness.generators)
                if k == g and len(witness.relators) > 0:
                    is_free = False
                else:
                    is_free = True
        else:
            is_free = False
            
        neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G is torsion-free",
    "¬Q: G is not a free group"
]

N_HYP = 2
NEG_Q_INDEX = 2