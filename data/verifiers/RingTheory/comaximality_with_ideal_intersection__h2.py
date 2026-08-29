import sympy
import itertools
import functools
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')

def parse_witness(witness):
    if isinstance(witness, dict):
        if 'elements' in witness:
            elements = witness['elements']
        elif 'R' in witness:
            elements = witness['R']
        elif 'n' in witness:
            elements = witness['n']
        else:
            raise ValueError("Missing elements/R/n in dict witness")
        add = witness['add']
        mul = witness['mul']
        I = witness['I']
        J = witness['J']
        K = witness['K']
    elif isinstance(witness, tuple):
        if len(witness) == 6:
            elements, add, mul, I, J, K = witness
        elif len(witness) == 4:
            R, I, J, K = witness
            elements = R.elements
            add = R.add
            mul = R.mul
        else:
            raise ValueError("Tuple witness must have length 4 or 6")
    else:
        elements = witness.elements
        add = witness.add
        mul = witness.mul
        I = witness.I
        J = witness.J
        K = witness.K

    if isinstance(elements, int):
        elements = list(range(elements))
    elif isinstance(elements, set):
        try:
            elements = sorted(list(elements))
        except Exception:
            elements = list(elements)
    else:
        elements = list(elements)

    if isinstance(add, dict):
        add_f = lambda a, b: add[(a, b)]
    elif not callable(add):
        add_f = lambda a, b: add[elements.index(a)][elements.index(b)]
    else:
        add_f = add

    if isinstance(mul, dict):
        mul_f = lambda a, b: mul[(a, b)]
    elif not callable(mul):
        mul_f = lambda a, b: mul[elements.index(a)][elements.index(b)]
    else:
        mul_f = mul

    return elements, add_f, mul_f, set(I), set(J), set(K)

def is_ideal(elements, add_f, mul_f, zero, S):
    if not S.issubset(set(elements)): return False
    if not S: return False
    # closed under addition
    for a in S:
        for b in S:
            if add_f(a, b) not in S: return False
    # closed under multiplication by R
    for a in S:
        for r in elements:
            if mul_f(a, r) not in S: return False
            if mul_f(r, a) not in S: return False
    # closed under negation (inverses)
    for a in S:
        inv = None
        for b in elements:
            if add_f(a, b) == zero:
                inv = b
                break
        if inv not in S: return False
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add_f, mul_f, I, J, K = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a commutative ring and I, J, K are ideals
    try:
        n = len(elements)
        if n == 0:
            h1 = False
        else:
            is_comm_ring = True
            for a in elements:
                for b in elements:
                    if add_f(a, b) != add_f(b, a): is_comm_ring = False
                    if mul_f(a, b) != mul_f(b, a): is_comm_ring = False
            
            if is_comm_ring:
                for a in elements:
                    for b in elements:
                        for c in elements:
                            if add_f(add_f(a, b), c) != add_f(a, add_f(b, c)): is_comm_ring = False
                            if mul_f(mul_f(a, b), c) != mul_f(a, mul_f(b, c)): is_comm_ring = False
                            if mul_f(a, add_f(b, c)) != add_f(mul_f(a, b), mul_f(a, c)): is_comm_ring = False
            
            if is_comm_ring:
                zeros = [z for z in elements if all(add_f(z, a) == a for a in elements)]
                if len(zeros) != 1:
                    is_comm_ring = False
                else:
                    zero = zeros[0]
                    for a in elements:
                        if not any(add_f(a, b) == zero for b in elements):
                            is_comm_ring = False
                            
            if is_comm_ring:
                h1 = is_ideal(elements, add_f, mul_f, zero, I) and \
                     is_ideal(elements, add_f, mul_f, zero, J) and \
                     is_ideal(elements, add_f, mul_f, zero, K)
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: I + J = R
    try:
        I_plus_J = {add_f(i, j) for i in I for j in J}
        h2 = (I_plus_J == set(elements))
    except Exception:
        h2 = False

    # H3: I + K = R
    try:
        I_plus_K = {add_f(i, k) for i in I for k in K}
        h3 = (I_plus_K == set(elements))
    except Exception:
        h3 = False

    # neg_Q: I + (J \cap K) != R
    try:
        J_cap_K = J.intersection(K)
        I_plus_J_cap_K = {add_f(i, x) for i in I for x in J_cap_K}
        neg_q = (I_plus_J_cap_K != set(elements))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring and I, J, K are ideals",
    "H_2: I and J are comaximal (I + J = R)",
    "H_3: I and K are comaximal (I + K = R)",
    "¬Q: I is not comaximal with J \\cap K (I + (J \\cap K) != R)"
]

N_HYP = 3
NEG_Q_INDEX = 3