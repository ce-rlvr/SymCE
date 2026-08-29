import sympy
from sympy import Symbol, sympify, Poly, isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
class Ring:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class Ideal:
    def __init__(self, ring, gens):
        self.ring = ring
        if not isinstance(gens, (list, tuple, set)):
            gens = [gens]
        self.gens = tuple(gens)

Z = Ring('Z')
Q = Ring('Q')
Zx = Ring('Z[x]')
Qx = Ring('Q[x]')

x = Symbol('x')

def get_attr(witness, attr):
    if isinstance(witness, dict):
        return witness.get(attr)
    return getattr(witness, attr, None)

def identify_ring(ring):
    if isinstance(ring, str):
        r = ring
    elif hasattr(ring, 'name'):
        r = ring.name
    else:
        r = str(ring)
    
    if r in ('Z', 'ZZ', 'Integers'):
        return 'Z'
    if r in ('Q', 'QQ', 'Rationals'):
        return 'Q'
    if r in ('Z[x]', 'ZZ[x]'):
        return 'Z[x]'
    if r in ('Q[x]', 'QQ[x]'):
        return 'Q[x]'
    return r

def identify_ideal(ideal):
    if hasattr(ideal, 'gens'):
        gens = ideal.gens
    elif isinstance(ideal, (list, tuple, set)):
        gens = list(ideal)
    else:
        gens = [ideal]
    
    norm_gens = []
    for g in gens:
        if hasattr(g, 'as_expr'):
            norm_gens.append(str(g.as_expr()))
        elif hasattr(g, 'name'):
            norm_gens.append(str(g.name))
        else:
            norm_gens.append(str(g))
    return norm_gens

def parse_gen(g):
    try:
        return int(g)
    except Exception:
        return sympify(g)

def is_comm_ring(r_name):
    return r_name in ['Z', 'Q', 'Z[x]', 'Q[x]']

def is_subring(r_name, s_name):
    if r_name == s_name:
        return True
    if r_name == 'Z' and s_name in ['Q', 'Z[x]', 'Q[x]']:
        return True
    if r_name == 'Q' and s_name == 'Q[x]':
        return True
    return False

def is_flat(r_name, s_name):
    if is_subring(r_name, s_name):
        return True
    return False

def is_prime_ideal(r_name, gens):
    if len(gens) != 1:
        return False
    g = gens[0]
    if r_name == 'Z':
        try:
            val = int(g)
            if val == 0:
                return True
            return isprime(abs(val))
        except Exception:
            return False
    if r_name == 'Q':
        try:
            val = int(g)
            return val == 0
        except Exception:
            return False
    return False

def is_subset_ideal(r_name, gens1, gens2):
    if r_name == 'Z':
        try:
            a = int(gens1[0])
            b = int(gens2[0])
            if b == 0:
                return a == 0
            return a % b == 0
        except Exception:
            return False
    if r_name == 'Q':
        try:
            a = int(gens1[0])
            b = int(gens2[0])
            if b == 0:
                return a == 0
            return True
        except Exception:
            return False
    return False

def is_in_ideal(s_name, elem, q2_gens):
    try:
        if s_name == 'Z[x]':
            if len(q2_gens) == 1:
                g = parse_gen(q2_gens[0])
                e = parse_gen(elem)
                if g == 0:
                    return e == 0
                if isinstance(g, int):
                    if isinstance(e, int):
                        return e % g == 0
                    else:
                        f = Poly(e, x)
                        return all(c % g == 0 for c in f.coeffs())
                else:
                    g_poly = Poly(g, x, domain='ZZ')
                    if isinstance(e, int):
                        if e == 0: return True
                        return False
                    e_poly = Poly(e, x, domain='ZZ')
                    q, r = e_poly.div(g_poly)
                    return r.is_zero
            elif len(q2_gens) == 2:
                p, f = q2_gens
                p = parse_gen(p)
                f = parse_gen(f)
                if not isinstance(p, int):
                    p, f = f, p
                e = parse_gen(elem)
                if isinstance(e, int):
                    return e % p == 0
                e_poly = Poly(e, x, domain='FF(' + str(p) + ')')
                f_poly = Poly(f, x, domain='FF(' + str(p) + ')')
                q, r = e_poly.div(f_poly)
                return r.is_zero
            else:
                return True
        elif s_name == 'Z':
            g = int(q2_gens[0])
            e = int(elem)
            if g == 0: return e == 0
            return e % g == 0
    except Exception:
        return True
    return True

def exists_q1(r_name, s_name, p1_gens, q2_gens):
    try:
        if r_name == 'Z' and s_name == 'Z[x]':
            p = int(p1_gens[0])
            if p == 0:
                return True
            else:
                return is_in_ideal('Z[x]', p, q2_gens)
        elif r_name == 'Z' and s_name == 'Q':
            p = int(p1_gens[0])
            if p == 0:
                return True
            else:
                return False
        elif r_name == 'Z' and s_name == 'Z':
            p = int(p1_gens[0])
            return is_in_ideal('Z', p, q2_gens)
        elif r_name == 'Q' and s_name == 'Q':
            p = int(p1_gens[0])
            if p == 0:
                return True
            return False
        elif r_name == 'Q' and s_name == 'Q[x]':
            p = int(p1_gens[0])
            if p == 0:
                return True
            return False
    except Exception:
        return True
    return True

def conditions(witness):
    try:
        R = get_attr(witness, 'R')
        S = get_attr(witness, 'S')
        P_1 = get_attr(witness, 'P_1')
        P_2 = get_attr(witness, 'P_2')
        Q_2 = get_attr(witness, 'Q_2')
        
        if R is None or S is None or P_1 is None or P_2 is None or Q_2 is None:
            return [False] * 4 + [False]

        r_name = identify_ring(R)
        s_name = identify_ring(S)
        p1_gens = identify_ideal(P_1)
        p2_gens = identify_ideal(P_2)
        q2_gens = identify_ideal(Q_2)
    except Exception:
        return [False] * 4 + [False]

    try:
        h1 = is_comm_ring(r_name) and is_comm_ring(s_name)
    except Exception:
        h1 = False

    try:
        h2 = is_subring(r_name, s_name)
    except Exception:
        h2 = False

    try:
        h3 = is_flat(r_name, s_name)
    except Exception:
        h3 = False

    try:
        h4 = is_prime_ideal(r_name, p1_gens) and is_prime_ideal(r_name, p2_gens) and is_subset_ideal(r_name, p1_gens, p2_gens)
    except Exception:
        h4 = False

    try:
        neg_q = not exists_q1(r_name, s_name, p1_gens, q2_gens)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: R is a subring of S",
    "H_3: S is a flat R-module",
    "H_4: P_1 and P_2 are prime ideals of R such that P_1 \\subseteq P_2",
    "¬Q: There does NOT exist a prime ideal Q_1 of S such that Q_1 \\subseteq Q_2 and Q_1 \\cap R = P_1"
]

N_HYP = 4
NEG_Q_INDEX = 4