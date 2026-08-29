import itertools
from sympy.ntheory import primefactors
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness objects
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
    # H1: f: R \to S is a ring homomorphism such that f(1_R) = 1_S
    try:
        R = witness.R
        S = witness.S
        
        f_attr = witness.f
        if callable(f_attr):
            f = f_attr
        elif isinstance(f_attr, dict):
            f = lambda x: f_attr[x]
        else:
            raise ValueError("f must be callable or a dict")
            
        add_R = getattr(witness, 'add_R', lambda a, b: a + b)
        mul_R = getattr(witness, 'mul_R', lambda a, b: a * b)
        add_S = getattr(witness, 'add_S', lambda a, b: a + b)
        mul_S = getattr(witness, 'mul_S', lambda a, b: a * b)
        
        R_sample = list(itertools.islice(R, 100))
        S_sample = list(itertools.islice(S, 100))
        
        one_R = getattr(witness, 'one_R', None)
        if one_R is None:
            for e in R_sample:
                if all(mul_R(e, a) == a and mul_R(a, e) == a for a in R_sample):
                    one_R = e
                    break
                    
        one_S = getattr(witness, 'one_S', None)
        if one_S is None:
            for e in S_sample:
                if all(mul_S(e, a) == a and mul_S(a, e) == a for a in S_sample):
                    one_S = e
                    break
                    
        if one_R is None or one_S is None:
            h1_ok = False
        elif f(one_R) != one_S:
            h1_ok = False
        else:
            h1_ok = True
            if isinstance(S, (list, set, tuple, dict)):
                for a in R_sample:
                    if f(a) not in S:
                        h1_ok = False
                        break
            if h1_ok:
                for a in R_sample:
                    fa = f(a)
                    for b in R_sample:
                        fb = f(b)
                        if f(add_R(a, b)) != add_S(fa, fb):
                            h1_ok = False
                            break
                        if f(mul_R(a, b)) != mul_S(fa, fb):
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
    except Exception:
        h1_ok = False

    # H2: R has a non-zero characteristic m
    try:
        R = witness.R
        m = witness.m
        if not isinstance(m, int) or m <= 0:
            h2_ok = False
        else:
            add_R = getattr(witness, 'add_R', lambda a, b: a + b)
            zero_R = getattr(witness, 'zero_R', None)
            R_sample = list(itertools.islice(R, 100))
            
            if zero_R is None:
                for z in R_sample:
                    if all(add_R(z, a) == a and add_R(a, z) == a for a in R_sample):
                        zero_R = z
                        break
            
            if zero_R is None:
                h2_ok = False
            else:
                def mult_add_R(k, a):
                    res = None
                    base = a
                    while k > 0:
                        if k % 2 == 1:
                            res = base if res is None else add_R(res, base)
                        base = add_R(base, base)
                        k //= 2
                    return res

                h2_ok = True
                for a in R_sample:
                    if mult_add_R(m, a) != zero_R:
                        h2_ok = False
                        break
                
                if h2_ok and m > 1:
                    for p in primefactors(m):
                        d = m // p
                        works = True
                        for a in R_sample:
                            if mult_add_R(d, a) != zero_R:
                                works = False
                                break
                        if works:
                            h2_ok = False
                            break
    except Exception:
        h2_ok = False

    # H3: S has a non-zero characteristic n
    try:
        S = witness.S
        n = witness.n
        if not isinstance(n, int) or n <= 0:
            h3_ok = False
        else:
            add_S = getattr(witness, 'add_S', lambda a, b: a + b)
            zero_S = getattr(witness, 'zero_S', None)
            S_sample = list(itertools.islice(S, 100))
            
            if zero_S is None:
                for z in S_sample:
                    if all(add_S(z, a) == a and add_S(a, z) == a for a in S_sample):
                        zero_S = z
                        break
            
            if zero_S is None:
                h3_ok = False
            else:
                def mult_add_S(k, a):
                    res = None
                    base = a
                    while k > 0:
                        if k % 2 == 1:
                            res = base if res is None else add_S(res, base)
                        base = add_S(base, base)
                        k //= 2
                    return res

                h3_ok = True
                for a in S_sample:
                    if mult_add_S(n, a) != zero_S:
                        h3_ok = False
                        break
                
                if h3_ok and n > 1:
                    for p in primefactors(n):
                        d = n // p
                        works = True
                        for a in S_sample:
                            if mult_add_S(d, a) != zero_S:
                                works = False
                                break
                        if works:
                            h3_ok = False
                            break
    except Exception:
        h3_ok = False

    # neg_Q: The characteristic n of S does NOT divide the characteristic m of R
    try:
        m = witness.m
        n = witness.n
        neg_q = (m % n != 0)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S such that f(1_R) = 1_S",
    "H_2: R has a non-zero characteristic m",
    "H_3: S has a non-zero characteristic n",
    "¬Q: The characteristic n of S does not divide the characteristic m of R"
]

N_HYP = 3
NEG_Q_INDEX = 3