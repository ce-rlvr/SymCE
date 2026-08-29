import sympy
from sympy import Rational

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
x, y, z = sympy.symbols('x y z')

def get_prime_factors(S):
    factors = set()
    for s in S:
        if s == 0:
            return {0}
        if s == 1 or s == -1:
            continue
        for p in sympy.factorint(abs(s)).keys():
            factors.add(p)
    return factors

def get_localization(n, S):
    if not isinstance(n, int) or n < 2:
        raise ValueError("n must be >= 2")
    M = set([1])
    queue = [1]
    while queue:
        curr = queue.pop(0)
        for s in S:
            nxt = (curr * (s % n)) % n
            if nxt not in M:
                M.add(nxt)
                queue.append(nxt)
    I_S = set()
    for x in range(n):
        for m in M:
            if (m * x) % n == 0:
                I_S.add(x)
                break
    cosets = {}
    for x in range(n):
        coset = frozenset((x + i) % n for i in I_S)
        cosets[x] = min(coset)
    return cosets, I_S

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'n'):
            n = witness.n
            S = witness.S
            T = witness.T
            T_bar = getattr(witness, 'T_bar', T)
        elif isinstance(witness, dict):
            n = witness.get('n', witness.get('R', None))
            S = witness['S']
            T = witness['T']
            T_bar = witness.get('T_bar', T)
        else:
            if len(witness) == 4:
                n, S, T, T_bar = witness
            elif len(witness) == 3:
                n, S, T = witness
                T_bar = T
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    if n is sympy.S.Integers or str(n) == 'ZZ':
        n = 0

    try:
        h1 = isinstance(n, int) and n >= 0
    except Exception:
        h1 = False

    try:
        if n == 0:
            h2 = set(T_bar) == set(T)
        else:
            cosets_S, I_S = get_localization(n, S)
            cosets_T = set(cosets_S[t % n] for t in T)
            cosets_T_bar = set(cosets_S[tb % n] for tb in T_bar)
            h2 = (cosets_T == cosets_T_bar)
    except Exception:
        h2 = False

    try:
        if n == 0:
            S_union_T = list(set(S) | set(T))
            ST = [s * t for s in S for t in T]
            factors1 = get_prime_factors(S_union_T)
            factors2 = get_prime_factors(ST)
            if 0 in factors1 and 0 in factors2:
                isomorphic = True
            elif 0 in factors1 or 0 in factors2:
                isomorphic = False
            else:
                isomorphic = (factors1 == factors2)
            neg_q = not isomorphic
        else:
            S_union_T = list(set(S) | set(T))
            _, I_S_union_T = get_localization(n, S_union_T)
            size_1 = n // len(I_S_union_T) if len(I_S_union_T) > 0 else 0
            
            ST = [(s * t) % n for s in S for t in T]
            _, I_ST = get_localization(n, ST)
            size_2 = n // len(I_ST) if len(I_ST) > 0 else 0
            
            neg_q = (size_1 != size_2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: T_bar is the image of T under the canonical ring homomorphism R -> S^{-1}R",
    "¬Q: The localized ring T_bar^{-1}(S^{-1}R) is NOT isomorphic to the localized ring (ST)^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2