import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard finite rings Z/nZ
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: f maps the multiplicative identity of R to the multiplicative identity of S",
    "H_3: Q is a primary ideal of S",
    "¬Q: The preimage of Q under f is not a primary ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        R, S, f, Q = witness
        
        # Parse R (modulus n)
        if hasattr(R, 'order') and callable(R.order):
            n = int(R.order())
        elif isinstance(R, int):
            n = R
        elif hasattr(R, '__len__'):
            n = len(R)
        else:
            n = int(R)
            
        # Parse S (modulus m)
        if hasattr(S, 'order') and callable(S.order):
            m = int(S.order())
        elif isinstance(S, int):
            m = S
        elif hasattr(S, '__len__'):
            m = len(S)
        else:
            m = int(S)
            
        # Parse f (mapping from R to S)
        if callable(f):
            f_dict = {x: f(x) for x in range(n)}
        elif isinstance(f, dict):
            f_dict = f
        elif isinstance(f, (list, tuple)):
            f_dict = {i: f[i] for i in range(len(f))}
        else:
            return [False, False, False, False]
            
        f_dict = {int(k): int(v) for k, v in f_dict.items()}
        
        # Parse Q (ideal of S)
        if isinstance(Q, int) or (hasattr(Q, 'is_Integer') and Q.is_Integer):
            g = math.gcd(m, int(Q))
            Q_set = { (g * i) % m for i in range(m) }
        else:
            Q_set = {int(q) for q in Q}
            
    except Exception:
        return [False, False, False, False]

    # H1: R and S are commutative rings with identity
    try:
        h1 = (n >= 2) and (m >= 2)
        if h1:
            if not all(k in f_dict for k in range(n)):
                h1 = False
            if not all(0 <= v < m for v in f_dict.values()):
                h1 = False
            if not all(0 <= q < m for q in Q_set):
                h1 = False
    except Exception:
        h1 = False

    # H2: f maps the multiplicative identity of R to the multiplicative identity of S
    try:
        h2 = False
        if h1:
            h2 = (f_dict[1] == 1)
    except Exception:
        h2 = False

    # H3: Q is a primary ideal of S
    try:
        h3 = False
        if h1:
            is_ideal = True
            if not Q_set:
                is_ideal = False
            else:
                for q1 in Q_set:
                    for q2 in Q_set:
                        if (q1 + q2) % m not in Q_set:
                            is_ideal = False
                    for s in range(m):
                        if (q1 * s) % m not in Q_set:
                            is_ideal = False
            
            is_primary = False
            if is_ideal and len(Q_set) < m:
                is_primary = True
                for a in range(m):
                    for b in range(m):
                        if (a * b) % m in Q_set:
                            if a not in Q_set:
                                b_k = b
                                found = False
                                for k in range(1, m + 1):
                                    if b_k in Q_set:
                                        found = True
                                        break
                                    b_k = (b_k * b) % m
                                if not found:
                                    is_primary = False
                                    break
                    if not is_primary:
                        break
            h3 = is_primary
    except Exception:
        h3 = False

    # neg_Q: The preimage of Q under f is not a primary ideal of R
    try:
        neg_q = False
        if h1:
            P_set = {x for x in range(n) if f_dict[x] in Q_set}
            
            is_P_ideal = True
            if not P_set:
                is_P_ideal = False
            else:
                for p1 in P_set:
                    for p2 in P_set:
                        if (p1 + p2) % n not in P_set:
                            is_P_ideal = False
                    for r in range(n):
                        if (p1 * r) % n not in P_set:
                            is_P_ideal = False
            
            is_P_primary = False
            if is_P_ideal and len(P_set) < n:
                is_P_primary = True
                for a in range(n):
                    for b in range(n):
                        if (a * b) % n in P_set:
                            if a not in P_set:
                                b_k = b
                                found = False
                                for k in range(1, n + 1):
                                    if b_k in P_set:
                                        found = True
                                        break
                                    b_k = (b_k * b) % n
                                if not found:
                                    is_P_primary = False
                                    break
                    if not is_P_primary:
                        break
            
            neg_q = not is_P_primary
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]