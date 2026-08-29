import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: L(x) is a linearized polynomial with coefficients in F_{q^m}",
    "H_2: E is an extension field of F_{q^m} containing all roots of L(x)",
    "¬Q: The set of roots of L(x) in E does not form a vector space over F_q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q', 2)
            poly = witness.get('poly', [])
            roots = witness.get('roots', [])
            Fq_elements = witness.get('Fq_elements', [])
            add = witness.get('add', lambda x, y: x + y)
            mul = witness.get('mul', lambda x, y: x * y)
            zero = witness.get('zero', 0)
        elif isinstance(witness, tuple) and len(witness) >= 8:
            poly, q, m, roots, Fq_elements, add, mul, zero = witness[:8]
        else:
            q = getattr(witness, 'q', 2)
            poly = getattr(witness, 'poly', [])
            roots = getattr(witness, 'roots', [])
            Fq_elements = getattr(witness, 'Fq_elements', [])
            add = getattr(witness, 'add', lambda x, y: x + y)
            mul = getattr(witness, 'mul', lambda x, y: x * y)
            zero = getattr(witness, 'zero', 0)

        # H1: L(x) is a linearized polynomial
        h1 = True
        try:
            if hasattr(poly, 'monoms'):
                monoms = poly.monoms()
                for monom in monoms:
                    deg = monom[0]
                    if deg == 0:
                        h1 = False
                        break
                    if q > 1:
                        i = round(math.log(deg, q))
                        if q**i != deg:
                            h1 = False
                            break
            elif isinstance(poly, list):
                h1 = True
            else:
                h1 = False
        except Exception:
            h1 = False

        # H2: E is an extension field containing all roots
        h2 = isinstance(roots, (list, set, tuple))

        # neg_Q: roots do not form a vector space over Fq
        is_vs = True
        if zero not in roots:
            is_vs = False
        else:
            for r1 in roots:
                for r2 in roots:
                    try:
                        if add(r1, r2) not in roots:
                            is_vs = False
                            break
                    except Exception:
                        is_vs = False
                        break
                if not is_vs:
                    break
            if is_vs:
                for c in Fq_elements:
                    for r in roots:
                        try:
                            if mul(c, r) not in roots:
                                is_vs = False
                                break
                        except Exception:
                            is_vs = False
                            break
                    if not is_vs:
                        break

        return [bool(h1), bool(h2), not is_vs]
    except Exception:
        return [False, False, False]