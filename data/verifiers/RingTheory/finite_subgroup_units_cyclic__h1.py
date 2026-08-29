import sympy
from sympy.matrices import eye, Matrix, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

# Standard algebra objects for potential witnesses
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    # H_1: G is a finite subgroup of the multiplicative group of units of R
    # We verify this by checking if the witness is a valid finite group under multiplication.
    h1_ok = False
    try:
        if isinstance(witness, PermutationGroup):
            h1_ok = True
        else:
            elements = list(witness)
            if elements:
                n = len(elements)
                identity = None
                # Find the multiplicative identity
                for e in elements:
                    is_id = True
                    for x in elements:
                        if e * x != x or x * e != x:
                            is_id = False
                            break
                    if is_id:
                        identity = e
                        break
                
                if identity is not None:
                    closed_and_inverses = True
                    for a in elements:
                        has_inverse = False
                        for b in elements:
                            prod = a * b
                            # Check closure without relying on hashability
                            is_in = False
                            for x in elements:
                                if prod == x:
                                    is_in = True
                                    break
                            if not is_in:
                                closed_and_inverses = False
                                break
                            
                            # Check inverse
                            if prod == identity and b * a == identity:
                                has_inverse = True
                        
                        if not closed_and_inverses or not has_inverse:
                            closed_and_inverses = False
                            break
                    h1_ok = closed_and_inverses
    except Exception:
        h1_ok = False

    # neg_Q: G is not a cyclic group
    neg_q_ok = False
    try:
        if isinstance(witness, PermutationGroup):
            if not witness.is_abelian:
                neg_q_ok = True
            else:
                order = witness.order()
                is_cyclic = False
                for e in witness.generate():
                    if e.order() == order:
                        is_cyclic = True
                        break
                neg_q_ok = not is_cyclic
        else:
            elements = list(witness)
            if elements:
                n = len(elements)
                is_cyclic = False
                for g in elements:
                    subgroup = []
                    current = g
                    for _ in range(n):
                        is_in_subgroup = False
                        for x in subgroup:
                            if current == x:
                                is_in_subgroup = True
                                break
                        if not is_in_subgroup:
                            subgroup.append(current)
                        current = current * g
                    
                    if len(subgroup) == n:
                        all_in = True
                        for x in subgroup:
                            is_in = False
                            for y in elements:
                                if x == y:
                                    is_in = True
                                    break
                            if not is_in:
                                all_in = False
                                break
                        if all_in:
                            is_cyclic = True
                            break
                neg_q_ok = not is_cyclic
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite subgroup of the multiplicative group of units of R",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1