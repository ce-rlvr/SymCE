import sympy
import math

def count_y(B, V, k, kD):
    if B == 0:
        return k if V % kD == 0 else 0
    
    B %= kD
    V %= kD
    g = math.gcd(B, kD)
    if V % g != 0:
        return 0
    
    B_prime = B // g
    V_prime = V // g
    m = kD // g
    
    y0 = (V_prime * pow(B_prime, -1, m)) % m
    
    if k <= y0:
        return 0
    return (k - 1 - y0) // m + 1

def to_sympy(val):
    if isinstance(val, (tuple, list)) and len(val) == 2:
        return sympy.Rational(val[0], val[1])
    try:
        return sympy.nsimplify(sympy.S(val))
    except Exception:
        return sympy.S(val)

def count_S(k, a, b, c):
    if k > 100000:
        raise ValueError("k is too large, preventing timeout")
        
    a = to_sympy(a)
    b = to_sympy(b)
    c = to_sympy(c)
    
    da = a.q if hasattr(a, 'q') else 1
    db = b.q if hasattr(b, 'q') else 1
    dc = c.q if hasattr(c, 'q') else 1
    
    D = sympy.lcm([da, db, dc])
    
    A = int(a * D)
    B = int(b * D)
    C = int(c * D)
    kD = int(k * D)
    
    count = 0
    for x in range(int(k)):
        V = C - A * x
        count += count_y(B, V, int(k), kD)
    return count

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness['m'], witness['n'], witness['a'], witness['b'], witness['c']
    elif hasattr(witness, 'm'):
        return witness.m, witness.n, witness.a, witness.b, witness.c
    return witness[0], witness[1], witness[2], witness[3], witness[4]

def conditions(witness) -> list[bool]:
    try:
        m, n, a, b, c = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H1: m and n are coprime positive integers
    try:
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0 and math.gcd(m, n) == 1
    except Exception:
        h1 = False
        
    # H2: S(k) denotes the number of pairs (x,y) in (Z/kZ)^2 satisfying ax + by = c mod k
    # We verify this by checking if a, b, c are valid numbers that can be evaluated.
    try:
        to_sympy(a)
        to_sympy(b)
        to_sympy(c)
        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: S(mn) != S(m)S(n)
    try:
        S_m = count_S(m, a, b, c)
        S_n = count_S(n, a, b, c)
        S_mn = count_S(m * n, a, b, c)
        neg_q = (S_mn != S_m * S_n)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are coprime positive integers",
    "H_2: S(k) denotes the number of pairs (x,y) in (Z/kZ)^2 satisfying ax + by = c mod k",
    "¬Q: S(mn) != S(m)S(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2