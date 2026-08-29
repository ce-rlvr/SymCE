import sympy
from sympy import Symbol, Poly

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is a maximal ideal of R",
    "H_3: P is a prime ideal of the polynomial ring over R",
    "not Q: P is not M polynomials and P is not a maximal ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3

def clean_generators(gens):
    if not isinstance(gens, (list, tuple)):
        gens = [gens]
    cleaned = []
    for g in gens:
        sg = sympy.sympify(g)
        if sg != 0:
            cleaned.append(sg)
    res = []
    for c in cleaned:
        if c not in res and -c not in res:
            res.append(c)
    if not res:
        return [sympy.sympify(0)]
    return res

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M', [])
            P = witness.get('P', [])
        else:
            R, M, P = witness
    except Exception:
        return [False, False, False, False]

    try:
        M_clean = clean_generators(M)
        P_clean = clean_generators(P)
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = (R in ['ZZ', 'QQ'])
    except Exception:
        h1 = False

    # H2: M is a maximal ideal of R
    try:
        h2 = False
        if R == 'ZZ':
            if len(M_clean) == 1:
                m = M_clean[0]
                if m.is_Integer and sympy.isprime(abs(int(m))):
                    h2 = True
        elif R == 'QQ':
            if len(M_clean) == 1 and M_clean[0] == 0:
                h2 = True
    except Exception:
        h2 = False

    # H3: P is a prime ideal of R[x]
    try:
        h3 = False
        if R == 'ZZ':
            if len(P_clean) == 1:
                f = P_clean[0]
                if f == 0:
                    h3 = True
                elif f.is_Integer:
                    h3 = sympy.isprime(abs(int(f)))
                else:
                    poly = Poly(f, x, domain='ZZ')
                    h3 = poly.is_primitive and poly.is_irreducible
            elif len(P_clean) == 2:
                f1, f2 = P_clean[0], P_clean[1]
                if f1.is_Integer and sympy.isprime(abs(int(f1))):
                    p, f = abs(int(f1)), f2
                elif f2.is_Integer and sympy.isprime(abs(int(f2))):
                    p, f = abs(int(f2)), f1
                else:
                    p, f = None, None
                if p is not None:
                    poly = Poly(f, x, domain=sympy.GF(p))
                    h3 = poly.is_irreducible
        elif R == 'QQ':
            if len(P_clean) == 1:
                f = P_clean[0]
                if f == 0:
                    h3 = True
                else:
                    poly = Poly(f, x, domain='QQ')
                    h3 = poly.is_irreducible
    except Exception:
        h3 = False

    # neg_Q: P != M[x] AND P is not a maximal ideal of R[x]
    try:
        neg_q = False
        if R == 'ZZ':
            m = M_clean[0] if M_clean else 0
            p_equals_mx = (len(P_clean) == 1 and P_clean[0] in [m, -m])
            p_is_maximal = (len(P_clean) == 2 and h3)
            neg_q = not (p_equals_mx or p_is_maximal)
        elif R == 'QQ':
            p_equals_mx = (len(P_clean) == 1 and P_clean[0] == 0)
            p_is_maximal = (len(P_clean) == 1 and P_clean[0] != 0 and h3)
            neg_q = not (p_equals_mx or p_is_maximal)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]