import sympy
from sympy import gcd, I, exp, pi, degree
from sympy.ntheory import totient
from sympy.polys import minpoly, cyclotomic_poly
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    "H_1: n and m are positive integers",
    "H_2: n and m are coprime",
    "H_3: ζ_m is a primitive m-th root of unity",
    "¬Q: The compositum field ℚ(ζ_n)ℚ(ζ_m) is not equal to ℚ(ζ_{nm})"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        n = witness.get('n')
        m = witness.get('m')
        zeta_n = witness.get('zeta_n')
        zeta_m = witness.get('zeta_m')
    else:
        try:
            n = witness[0]
            m = witness[1]
            zeta_n = witness[2]
            zeta_m = witness[3]
        except (IndexError, TypeError):
            return [False, False, False, False]

    # H_1: n and m are positive integers
    try:
        h1 = (int(n) == n) and (int(m) == m) and (n > 0) and (m > 0)
    except Exception:
        h1 = False

    # H_2: n and m are coprime
    try:
        h2 = bool(gcd(n, m) == 1)
    except Exception:
        h2 = False

    # H_3: ζ_m is a primitive m-th root of unity
    try:
        m_int = int(m)
        mp = minpoly(zeta_m, x)
        cp = cyclotomic_poly(m_int, x)
        h3 = bool((mp - cp).expand() == 0)
    except Exception:
        h3 = False

    # ¬Q: The compositum field ℚ(ζ_n)ℚ(ζ_m) is not equal to ℚ(ζ_{nm})
    # We check if the degree of ℚ(ζ_n, ζ_m) over ℚ is different from totient(n*m).
    try:
        best_deg = 0
        for c in range(1, 6):
            elem = zeta_n + c * zeta_m
            mp_elem = minpoly(elem, x)
            deg = degree(mp_elem, x)
            if deg > best_deg:
                best_deg = deg
        
        expected_deg = totient(int(n) * int(m))
        neg_q = bool(best_deg != expected_deg)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]