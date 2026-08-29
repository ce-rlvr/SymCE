import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    "H_1: G has no non-trivial abelian normal subgroups",
    "¬Q: The center of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            h1_ok = False
        elif witness.order() == 1:
            h1_ok = True
        else:
            h1_ok = True
            gens = witness.generators
            id_perm = gens[0] * ~gens[0]
            
            count = 0
            for g in witness.generate():
                if g == id_perm:
                    continue
                count += 1
                if count > 2000:
                    break
                    
                conjugates = set([g])
                queue = [g]
                is_abelian = True
                
                # Compute the normal closure of <g> on the fly.
                # If all elements in the conjugacy class of g commute with each other,
                # then the normal closure is an abelian normal subgroup.
                while queue and is_abelian:
                    curr = queue.pop(0)
                    for gen in gens:
                        for conj_op in (gen, ~gen):
                            conj = conj_op * curr * ~conj_op
                            if conj not in conjugates:
                                # Check if the new conjugate commutes with all existing ones
                                for c in conjugates:
                                    if conj * c != c * conj:
                                        is_abelian = False
                                        break
                                if not is_abelian:
                                    break
                                conjugates.add(conj)
                                queue.append(conj)
                        if not is_abelian:
                            break
                            
                if is_abelian:
                    # Found a non-trivial abelian normal subgroup
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q_ok = False
        else:
            C = witness.center()
            neg_q_ok = C.order() > 1
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]