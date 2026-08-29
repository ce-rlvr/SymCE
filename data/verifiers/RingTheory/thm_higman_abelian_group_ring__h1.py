import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import functools

# Top-level setup: Standard groups that might be used as witnesses
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Construct the Quaternion group Q8 as a permutation group
_p_i = Permutation(0, 2, 1, 3)(4, 6, 5, 7)
_p_j = Permutation(0, 4, 1, 5)(2, 7, 3, 6)
Q8 = PermutationGroup(_p_i, _p_j)

def conditions(witness):
    # H_1: G is a group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails
    # Conclusion: U(ZG) is finite iff G is an elementary abelian 2-group or cyclic of order 1, 2, 3, 4, 6
    try:
        elements = list(witness.elements)
        n = len(elements)
        orders = [int(g.order()) for g in elements]
        exp = int(functools.reduce(sympy.lcm, orders, 1))
        
        # Check if U(ZG) is finite (Higman's Theorem)
        if witness.is_abelian:
            u_finite = (exp in (1, 2, 3, 4, 6))
        else:
            # For non-abelian groups, U(ZG) is finite iff G is a Hamiltonian 2-group (Q8 x E)
            if exp != 4:
                u_finite = False
            else:
                u_finite = True
                for g in elements:
                    g_pow = set()
                    curr = g**0
                    for _ in range(int(g.order())):
                        g_pow.add(curr)
                        curr = curr * g
                    # Check if every cyclic subgroup is normal
                    for h in elements:
                        if h * g * h**-1 not in g_pow:
                            u_finite = False
                            break
                    if not u_finite:
                        break
                        
        # Check if G is an elementary abelian 2-group or cyclic of order 1, 2, 3, 4, 6
        if not witness.is_abelian:
            is_special = False
        else:
            if exp in (1, 2):
                is_special = True
            elif n in (1, 2, 3, 4, 6):
                is_special = any(int(g.order()) == n for g in elements)
            else:
                is_special = False
                
        # The conjecture claims u_finite == is_special. We want the negation.
        neg_q_ok = bool(u_finite != is_special)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: U(ZG) is finite iff G is elementary abelian 2-group or cyclic of order 1, 2, 3, 4, 6 FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1