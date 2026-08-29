import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
            add = witness.get('add', lambda x, y: x + y)
            mul = witness.get('mul', lambda x, y: x * y)
            zero = witness.get('zero', 0)
        elif isinstance(witness, tuple) and len(witness) == 3:
            if all(isinstance(x, int) for x in witness):
                n, a, b = witness
                if n <= 0:
                    return [False, False, False]
                a = math.gcd(a, n)
                b = math.gcd(b, n)
                h1 = True
                h2 = True
                ab = math.gcd(a * b, n)
                lcm_ab = math.gcd((a * b) // math.gcd(a, b), n)
                is_subset = (ab % lcm_ab == 0)
                neg_q = not is_subset
                return [h1, h2, neg_q]
            else:
                R, I, J = witness
                add = lambda x, y: x + y
                mul = lambda x, y: x * y
                zero = 0
        else:
            R = witness.R
            I = witness.I
            J = witness.J
            add = getattr(witness, 'add', lambda x, y: x + y)
            mul = getattr(witness, 'mul', lambda x, y: x * y)
            zero = getattr(witness, 'zero', 0)

        R_list = []
        for i, r in enumerate(R):
            if i > 1000: return [False, False, False]
            R_list.append(r)
        R = R_list

        I_list = []
        for i, x in enumerate(I):
            if i > 1000: return [False, False, False]
            I_list.append(x)
        I = I_list

        J_list = []
        for i, x in enumerate(J):
            if i > 1000: return [False, False, False]
            J_list.append(x)
        J = J_list

        def safe_eq(a, b):
            try:
                return a == b
            except Exception:
                return False

        def is_ideal(S_list):
            for x in S_list:
                if not any(safe_eq(x, r) for r in R): return False
            if not any(safe_eq(zero, x) for x in S_list): return False
            for x in S_list:
                for y in S_list:
                    s = add(x, y)
                    if not any(safe_eq(s, z) for z in S_list): return False
            for s in S_list:
                for r in R:
                    m1 = mul(r, s)
                    if not any(safe_eq(m1, z) for z in S_list): return False
                    m2 = mul(s, r)
                    if not any(safe_eq(m2, z) for z in S_list): return False
            return True

        h1 = is_ideal(I)
        h2 = is_ideal(J)

        products = []
        for a in I:
            for b in J:
                p = mul(a, b)
                if not any(safe_eq(p, x) for x in products):
                    products.append(p)
        
        closure = list(products)
        added = True
        while added:
            added = False
            new_elements = []
            for x in closure:
                for y in closure:
                    s = add(x, y)
                    if not any(safe_eq(s, z) for z in closure) and not any(safe_eq(s, z) for z in new_elements):
                        new_elements.append(s)
            if new_elements:
                closure.extend(new_elements)
                added = True
                if len(closure) > 1000:
                    return [False, False, False]

        IJ = closure
        I_cap_J = [x for x in I if any(safe_eq(x, y) for y in J)]

        is_subset = True
        for x in IJ:
            if not any(safe_eq(x, y) for y in I_cap_J):
                is_subset = False
                break
        
        neg_q = not is_subset

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        if hasattr(witness, 'I') and hasattr(witness, 'J'):
            I = witness.I
            J = witness.J
            if type(I).__name__ == 'Ideal' and type(J).__name__ == 'Ideal':
                h1 = True
                h2 = True
                IJ = I * J
                I_cap_J = I.intersect(J)
                is_subset = IJ.subset(I_cap_J)
                neg_q = not is_subset
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS: list[str] = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: The product ideal IJ is not a subset of I \\cap J"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2