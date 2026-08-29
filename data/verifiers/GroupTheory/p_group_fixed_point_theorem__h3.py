import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
import itertools

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

def conditions(witness):
    try:
        if len(witness) == 4:
            p, G, X, action = witness
        elif len(witness) == 3:
            p, G, X = witness
            if hasattr(X, 'action'):
                action = X.action
            elif hasattr(X, 'act'):
                action = X.act
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H2: G is a finite p-group
    try:
        order = G.order()
        if order == 1:
            h2 = True
        else:
            factors = sympy.factorint(order)
            h2 = (list(factors.keys()) == [p])
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        elements = list(G.elements)
        identity = G.identity

        is_finite = False
        if isinstance(X, str):
            is_finite = False
        elif isinstance(X, (list, set, tuple, frozenset, range)):
            if len(X) <= 10000:
                X_list = list(X)
                is_finite = True
            else:
                return [False, False, False, False]
        else:
            try:
                length = len(X)
                if length <= 10000:
                    X_list = list(X)
                    is_finite = True
                else:
                    return [False, False, False, False]
            except Exception:
                is_finite = False

        if is_finite:
            h3 = True
            for x in X_list:
                if action(identity, x) != x:
                    h3 = False
                    break
                for g in elements:
                    res = action(g, x)
                    if res not in X_list:
                        h3 = False
                        break
                    for h in elements:
                        if action(g, action(h, x)) != action(g*h, x):
                            h3 = False
                            break
                    if not h3: break
                if not h3: break
        else:
            h3 = False
            # Symbolic check for infinite sets
            x_sym, y_sym, z_sym = sympy.symbols('x y z')
            points_to_try = [x_sym, (x_sym, y_sym), (x_sym, y_sym, z_sym)]
            
            valid_point = None
            for pt in points_to_try:
                try:
                    res = action(identity, pt)
                    if isinstance(pt, tuple):
                        if isinstance(res, tuple) and len(res) == len(pt):
                            diffs = [sympy.simplify(r - p_i) for r, p_i in zip(res, pt)]
                            if all(d == 0 for d in diffs):
                                valid_point = pt
                                break
                    else:
                        try:
                            diff = res - pt
                            if diff == 0 or sympy.simplify(diff) == 0:
                                valid_point = pt
                                break
                        except Exception:
                            if res == pt:
                                valid_point = pt
                                break
                except Exception:
                    continue
                    
            if valid_point is not None:
                h3 = True
                pt = valid_point
                for g in elements:
                    for h in elements:
                        try:
                            lhs = action(g, action(h, pt))
                            rhs = action(g*h, pt)
                            if isinstance(pt, tuple):
                                if not isinstance(lhs, tuple) or not isinstance(rhs, tuple):
                                    h3 = False
                                    break
                                for l, r in zip(lhs, rhs):
                                    try:
                                        diff = l - r
                                        if diff != 0 and sympy.simplify(diff) != 0:
                                            h3 = False
                                            break
                                    except Exception:
                                        if l != r:
                                            h3 = False
                                            break
                                if not h3: break
                            else:
                                try:
                                    diff = lhs - rhs
                                    if diff != 0 and sympy.simplify(diff) != 0:
                                        h3 = False
                                        break
                                except Exception:
                                    if lhs != rhs:
                                        h3 = False
                                        break
                        except Exception:
                            h3 = False
                            break
                    if not h3: break

            if not h3:
                # Fallback 1: integers
                h3_fallback = True
                for pt in range(-10, 11):
                    try:
                        if action(identity, pt) != pt:
                            h3_fallback = False
                            break
                        for g in elements:
                            for h in elements:
                                if action(g, action(h, pt)) != action(g*h, pt):
                                    h3_fallback = False
                                    break
                            if not h3_fallback: break
                    except Exception:
                        h3_fallback = False
                        break
                if h3_fallback:
                    h3 = True

            if not h3:
                # Fallback 2: integer tuples
                h3_fallback = True
                for pt in itertools.product(range(-3, 4), repeat=2):
                    try:
                        if action(identity, pt) != pt:
                            h3_fallback = False
                            break
                        for g in elements:
                            for h in elements:
                                if action(g, action(h, pt)) != action(g*h, pt):
                                    h3_fallback = False
                                    break
                            if not h3_fallback: break
                    except Exception:
                        h3_fallback = False
                        break
                if h3_fallback:
                    h3 = True

    except Exception:
        h3 = False

    # neg_Q: |X| \not\equiv |X^G| \pmod p
    try:
        if is_finite:
            fixed_count = 0
            for x in X_list:
                is_fixed = True
                for g in elements:
                    if action(g, x) != x:
                        is_fixed = False
                        break
                if is_fixed:
                    fixed_count += 1
            
            size_X = len(X_list)
            q_holds = (size_X % p) == (fixed_count % p)
            neg_q = not q_holds
        else:
            # Infinite set, conclusion is false/undefined
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "H_3: G acts on X",
    "¬Q: |X| is not congruent to |X^G| mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3