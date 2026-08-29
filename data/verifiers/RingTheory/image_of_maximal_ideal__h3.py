import math
import itertools
import functools
import sympy
from sympy import symbols, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import z3

# Top-level setup
Z = 0
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

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2_group = CyclicGroup(2)
Z3_group = CyclicGroup(3)
Z4_group = CyclicGroup(4)
Z6_group = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def parse_ring(x):
    if isinstance(x, str):
        x = x.strip().upper()
        if x == 'Z':
            return 0
        if x.startswith('Z'):
            try:
                return int(x[1:])
            except Exception:
                pass
    return int(x)

def get_generator(a, n):
    if isinstance(a, str):
        a = a.strip('()[]{} ')
        if ',' in a:
            a = [x.strip() for x in a.split(',')]
    
    if isinstance(a, (list, tuple, set)):
        gen = 0
        for x in a:
            gen = math.gcd(gen, abs(int(x)))
        return gen
    else:
        return abs(int(a))

def parse_witness(witness):
    if isinstance(witness, dict):
        n = witness.get('R', witness.get('r', witness.get('n', None)))
        m = witness.get('S', witness.get('s', witness.get('m', None)))
        a = witness.get('M', witness.get('a', witness.get('ideal', None)))
        if n is None or m is None or a is None:
            raise ValueError("Missing keys in dict")
        return n, m, a
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
        elif len(witness) == 4:
            return witness[0], witness[1], witness[3]
    raise ValueError("Invalid witness format")

def conditions(witness) -> list[bool]:
    try:
        n_raw, m_raw, a_raw = parse_witness(witness)
        n = abs(parse_ring(n_raw))
        m = abs(parse_ring(m_raw))
        a = get_generator(a_raw, n)
    except Exception:
        return [False, False, False, False]

    # H1: R and S are commutative rings
    try:
        # Our representation only covers Z/nZ, which are always commutative rings.
        h1 = isinstance(n, int) and isinstance(m, int)
    except Exception:
        h1 = False

    # H2: f: R \to S is a surjective ring homomorphism
    try:
        if n == 0:
            h2 = True
        else:
            h2 = (m > 0 and n % m == 0)
    except Exception:
        h2 = False

    # H3: The kernel of f is contained in M
    try:
        if n == 0:
            if a == 0:
                h3 = (m == 0)
            else:
                h3 = (m % a == 0)
        else:
            g = math.gcd(a, n)
            h3 = (m % g == 0)
    except Exception:
        h3 = False

    # neg_Q: The image f(M) is NOT a maximal ideal of S
    try:
        gen_S = math.gcd(a, m)
        is_maximal = isprime(gen_S)
        neg_q = not is_maximal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R \\to S is a surjective ring homomorphism",
    "H_3: The kernel of f is contained in M",
    "¬Q: The image f(M) is not a maximal ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3