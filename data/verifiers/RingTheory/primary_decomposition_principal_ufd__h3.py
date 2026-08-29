import sympy
from sympy import isprime, simplify
from sympy.polys.polytools import factor_list
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
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

def is_integer_type(val):
    if isinstance(val, int):
        return True
    if hasattr(val, 'is_integer'):
        res = val.is_integer() if callable(val.is_integer) else val.is_integer
        if res is True:
            return True
    return False

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the element `a`, and the proposed primary decomposition
    components `p_list` and `e_list`.
    Format: tuple (a, p_list, e_list) or dict {'a': a, 'p_list': [...], 'e_list': [...]}
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            p_list = witness.get('p_list', [])
            e_list = witness.get('e_list', [])
        else:
            a, p_list, e_list = witness
    except Exception:
        return [False, False, False]

    # H1: R is a Unique Factorization Domain
    # We evaluate over Z (integers) or Q[x] (sympy expressions), both of which are UFDs.
    try:
        h1 = is_integer_type(a) or isinstance(a, sympy.Expr)
    except Exception:
        h1 = False

    # H2: a is a non-zero, non-unit element of R
    try:
        if is_integer_type(a):
            val = abs(int(a))
            h2 = val != 0 and val != 1
        elif isinstance(a, sympy.Expr):
            h2 = a != 0 and not a.is_constant()
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The irredundant primary decomposition of (a) is NOT given by the intersection (p_1^{e_1}) \cap \cdots \cap (p_k^{e_k})
    try:
        if len(p_list) != len(e_list):
            neg_q = True
        else:
            is_decomp = True
            if is_integer_type(a):
                for p, e in zip(p_list, e_list):
                    if not is_integer_type(p) or not is_integer_type(e):
                        is_decomp = False
                        break
                    if not isprime(abs(int(p))):
                        is_decomp = False
                        break
                    if int(e) < 1:
                        is_decomp = False
                        break
                
                if is_decomp:
                    radicals = [abs(int(p)) for p in p_list]
                    if len(set(radicals)) != len(radicals):
                        is_decomp = False
                
                if is_decomp:
                    prod = 1
                    for p, e in zip(p_list, e_list):
                        prod *= abs(int(p))**int(e)
                    if prod != abs(int(a)):
                        is_decomp = False
            else:
                for p, e in zip(p_list, e_list):
                    if not is_integer_type(e) or int(e) < 1:
                        is_decomp = False
                        break
                    try:
                        factors = factor_list(p)
                        if len(factors[1]) != 1 or factors[1][0][1] != 1:
                            is_decomp = False
                            break
                    except Exception:
                        is_decomp = False
                        break
                
                if is_decomp:
                    radicals = []
                    for p in p_list:
                        factors = factor_list(p)
                        radicals.append(factors[1][0][0])
                    
                    for i in range(len(radicals)):
                        for j in range(i+1, len(radicals)):
                            if simplify(radicals[i] - radicals[j]) == 0:
                                is_decomp = False
                                break
                        if not is_decomp:
                            break
                
                if is_decomp:
                    prod = 1
                    for p, e in zip(p_list, e_list):
                        prod *= p**int(e)
                    ratio = simplify(a / prod)
                    if not ratio.is_constant() or ratio == 0:
                        is_decomp = False

            neg_q = not is_decomp
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a is a non-zero, non-unit element of R",
    "¬Q: The irredundant primary decomposition of (a) is NOT given by the intersection (p_1^{e_1}) \\cap \\cdots \\cap (p_k^{e_k})"
]

N_HYP = 2
NEG_Q_INDEX = 2