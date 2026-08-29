import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_p_q(n):
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0
    for _ in range(n + 1):
        p_curr = p_prev1 + p_prev2
        q_curr = q_prev1 + q_prev2
        p_prev2, p_prev1 = p_prev1, p_curr
        q_prev2, q_prev1 = q_prev1, q_curr
    return p_prev1, q_prev1

def fibonacci(n):
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def conditions(witness) -> list[bool]:
    h1 = True
    h2 = True
    neg_q = False

    # If witness is a dictionary containing 'p' and 'q'
    if isinstance(witness, dict) and ('p' in witness or 'q' in witness):
        p = witness.get('p')
        q = witness.get('q')
        
        if 'x' in witness:
            try:
                x = witness['x']
                h1 = all(x[i] == 1 for i in range(5))
            except Exception:
                h1 = False
                
        if 'F' in witness:
            try:
                F = witness['F']
                h2 = (F[0] == 0 and F[1] == 1 and F[2] == 1 and F[3] == 2)
            except Exception:
                h2 = False
                
        if p is not None and q is not None:
            for n in range(10):
                try:
                    pn = p(n) if callable(p) else p[n]
                    qn = q(n) if callable(q) else q[n]
                    if pn != fibonacci(n+2) or qn != fibonacci(n+1):
                        neg_q = True
                        break
                except Exception:
                    neg_q = True
                    break
            return [h1, h2, neg_q]

    # If witness is a tuple (x, F, p, q) or (p, q)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            p, q = witness
            for n in range(10):
                try:
                    pn = p(n) if callable(p) else p[n]
                    qn = q(n) if callable(q) else q[n]
                    if pn != fibonacci(n+2) or qn != fibonacci(n+1):
                        neg_q = True
                        break
                except Exception:
                    neg_q = True
                    break
            return [h1, h2, neg_q]
        elif len(witness) == 4:
            x, F, p, q = witness
            try:
                h1 = all(x[i] == 1 for i in range(5))
            except Exception:
                h1 = False
            try:
                h2 = (F[0] == 0 and F[1] == 1 and F[2] == 1 and F[3] == 2)
            except Exception:
                h2 = False
            for n in range(10):
                try:
                    pn = p(n) if callable(p) else p[n]
                    qn = q(n) if callable(q) else q[n]
                    if pn != fibonacci(n+2) or qn != fibonacci(n+1):
                        neg_q = True
                        break
                except Exception:
                    neg_q = True
                    break
            return [h1, h2, neg_q]

    # Otherwise, assume witness is n
    try:
        if not (witness >= 0):
            neg_q = False
            return [h1, h2, neg_q]
            
        is_int = False
        if isinstance(witness, int):
            is_int = True
        elif isinstance(witness, float):
            is_int = witness.is_integer()
        elif hasattr(witness, 'is_integer'):
            prop = witness.is_integer
            if callable(prop):
                is_int = prop()
            else:
                is_int = bool(prop)
                
        if is_int:
            n_int = int(witness)
            if n_int > 100000:
                neg_q = False
            else:
                p_n, q_n = get_p_q(n_int)
                neg_q = not (p_n == fibonacci(n_int+2) and q_n == fibonacci(n_int+1))
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is the infinite simple continued fraction with all partial quotients equal to 1",
    "H_2: F_n is the n-th Fibonacci number, defined by F_0=0, F_1=1, and F_n = F_{n-1} + F_{n-2}",
    "not Q: It is not the case that for all n >= 0, p_n = F_{n+2} and q_n = F_{n+1}"
]

N_HYP = 2
NEG_Q_INDEX = 2