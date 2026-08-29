import sympy
from sympy import ZZ, QQ

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture:
    Hypotheses:
      - R is a commutative ring
      - S is a multiplicatively closed subset of R
      - a is an element of R
    Conclusion:
      The fraction a/s is a unit in S^{-1}R if and only if there exists an element b in R such that ab is in S.
      
    The dropped hypothesis from the true theorem is "s is an element of S".
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            a = witness.get('a')
            s = witness.get('s')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            R, S, a, s = witness
        else:
            return [False, False, False, False]

        is_finite = False
        is_known_ring = False
        R_elements = []
        
        # Determine ring structure
        if isinstance(R, int) and R > 1:
            n = R
            R_elements = list(range(n))
            add_op = lambda x, y: (x + y) % n
            mul_op = lambda x, y: (x * y) % n
            zero = 0
            is_finite = True
            is_known_ring = True
        elif isinstance(R, (list, tuple, set)):
            R_elements = list(R)
            is_finite = True
            if all(isinstance(x, (int, sympy.Integer)) for x in R_elements) and sorted([int(x) for x in R_elements]) == list(range(len(R_elements))):
                n = len(R_elements)
                add_op = lambda x, y: (int(x) + int(y)) % n
                mul_op = lambda x, y: (int(x) * int(y)) % n
                zero = 0
                is_known_ring = True
            else:
                add_op = lambda x, y: x + y
                mul_op = lambda x, y: x * y
                zero = None
                for x in R_elements:
                    if all(add_op(x, y) == y for y in R_elements):
                        zero = x
                        break
                if zero is None:
                    return [False, False, False, False]
        elif R == ZZ or R == QQ:
            add_op = lambda x, y: x + y
            mul_op = lambda x, y: x * y
            zero = 0
            is_finite = False
        else:
            return [False, False, False, False]

        # H1: R is a commutative ring
        h1 = False
        if is_finite:
            if is_known_ring:
                h1 = True
            elif len(R_elements) <= 50:
                h1 = True
                for x in R_elements:
                    for y in R_elements:
                        if add_op(x, y) not in R_elements: h1 = False
                        if mul_op(x, y) not in R_elements: h1 = False
                        if add_op(x, y) != add_op(y, x): h1 = False
                        if mul_op(x, y) != mul_op(y, x): h1 = False
                if h1:
                    for x in R_elements:
                        if add_op(x, zero) != x: h1 = False
                        has_inv = False
                        for y in R_elements:
                            if add_op(x, y) == zero:
                                has_inv = True
                                break
                        if not has_inv: h1 = False
                if h1:
                    for x in R_elements:
                        for y in R_elements:
                            for z in R_elements:
                                if add_op(add_op(x, y), z) != add_op(x, add_op(y, z)): h1 = False
                                if mul_op(mul_op(x, y), z) != mul_op(x, mul_op(y, z)): h1 = False
                                if mul_op(x, add_op(y, z)) != add_op(mul_op(x, y), mul_op(x, z)): h1 = False
            else:
                h1 = False
        else:
            if R == ZZ or R == QQ:
                h1 = True

        # H2: S is a multiplicatively closed subset of R
        S_list = list(S)
        h2 = len(S_list) > 0
        if h2:
            if is_finite:
                for x in S_list:
                    if x not in R_elements:
                        h2 = False
                        break
            else:
                if R == ZZ:
                    for x in S_list:
                        if not (isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)):
                            h2 = False
                            break
                elif R == QQ:
                    for x in S_list:
                        if not (isinstance(x, (int, float)) or hasattr(x, 'is_rational')):
                            h2 = False
                            break
            if h2:
                for x in S_list:
                    for y in S_list:
                        if mul_op(x, y) not in S_list:
                            h2 = False
                            break
                    if not h2: break

        # H3: a is an element of R
        h3 = False
        if is_finite:
            h3 = a in R_elements
        else:
            if R == ZZ:
                h3 = isinstance(a, int) or (hasattr(a, 'is_integer') and a.is_integer)
            elif R == QQ:
                h3 = isinstance(a, (int, float)) or hasattr(a, 'is_rational')

        # RHS: exists b in R such that ab in S
        rhs = False
        if is_finite:
            for b in R_elements:
                if is_known_ring:
                    if (int(a) * int(b)) % n in S_list:
                        rhs = True
                        break
                else:
                    if mul_op(a, b) in S_list:
                        rhs = True
                        break
        else:
            if R == ZZ:
                if a != 0:
                    for x in S_list:
                        if x % a == 0:
                            rhs = True
                            break
                else:
                    if 0 in S_list:
                        rhs = True
            elif R == QQ:
                if a != 0:
                    rhs = True
                else:
                    if 0 in S_list:
                        rhs = True

        # LHS: a/s is a unit in S^{-1}R
        # If s is in S, the equivalence mathematically holds for any commutative ring.
        # If s is not in S, a/s is not an element of S^{-1}R, so it cannot be a unit.
        if s in S_list:
            lhs = rhs
        else:
            lhs = False

        neg_q = (lhs != rhs)

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: a is an element of R",
    "¬Q: The equivalence between a/s being a unit and exists b such that ab in S fails"
]

N_HYP = 3
NEG_Q_INDEX = 3