import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            if 'table' in witness:
                M = witness['table']
                elements = list(range(len(M)))
                def mul(x, y): return M[x][y]
                provided_U = witness.get('U', None)
            else:
                return [False, False, False]
        elif isinstance(witness, (list, tuple)) and all(isinstance(row, (list, tuple)) for row in witness):
            M = witness
            elements = list(range(len(M)))
            def mul(x, y): return M[x][y]
            provided_U = None
        else:
            elements = list(witness.elements)
            mul = witness.mul
            provided_U = getattr(witness, 'U', None)

        # H1: R has a multiplicative identity 1
        has_id = False
        identity = None
        for e in elements:
            if all(mul(e, x) == x and mul(x, e) == x for x in elements):
                has_id = True
                identity = e
                break

        # H2: U(R) is the set of all elements in R that have a two-sided multiplicative inverse
        computed_U = []
        if has_id:
            for x in elements:
                has_inv = False
                for y in elements:
                    if mul(x, y) == identity and mul(y, x) == identity:
                        has_inv = True
                        break
                if has_inv:
                    computed_U.append(x)
        
        if provided_U is not None:
            h2_ok = set(computed_U) == set(provided_U)
            U = list(provided_U)
        else:
            h2_ok = True
            U = computed_U

        # neg_Q: U(R) does not form a group under ring multiplication
        is_group = True
        if not has_id:
            is_group = False
        else:
            # Check closure
            for x in U:
                for y in U:
                    if mul(x, y) not in U:
                        is_group = False
                        break
                if not is_group:
                    break
            
            # Check associativity on U
            if is_group:
                for x in U:
                    for y in U:
                        for z in U:
                            if mul(mul(x, y), z) != mul(x, mul(y, z)):
                                is_group = False
                                break
                        if not is_group: break
                    if not is_group: break

        neg_q = not is_group

        return [has_id, h2_ok, neg_q]

    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity 1",
    "H_2: U(R) is the set of all elements in R that have a two-sided multiplicative inverse",
    "¬Q: U(R) does not form a group under ring multiplication"
]

N_HYP = 2
NEG_Q_INDEX = 2