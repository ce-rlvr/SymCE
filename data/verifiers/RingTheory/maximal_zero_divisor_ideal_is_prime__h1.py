import sympy
from sympy import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Z is the set of all zero divisors of R",
    "H_2: I is an ideal of R such that I is a subset of Z",
    "H_3: For any ideal J of R strictly containing I, J is not a subset of Z",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Extract witness components
    try:
        if isinstance(witness, dict):
            n = int(witness['n'])
            add = witness['add']
            mult = witness['mult']
            I = witness['I']
            Z_wit = witness['Z']
        else:
            n = int(witness.n)
            add = witness.add
            mult = witness.mult
            I = witness.I
            Z_wit = witness.Z
            
        I_set = set(int(x) for x in I)
        Z_set = set(int(x) for x in Z_wit)
    except Exception:
        return [False, False, False, False]

    # Helper function to validate ring axioms
    def is_ring():
        if not isinstance(n, int) or n <= 0: return False
        if len(add) != n or len(mult) != n: return False
        for i in range(n):
            if len(add[i]) != n or len(mult[i]) != n: return False
            for j in range(n):
                if not (0 <= add[i][j] < n): return False
                if not (0 <= mult[i][j] < n): return False
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False
                    if mult[mult[i][j]][k] != mult[i][mult[j][k]]: return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mult[i][add[j][k]] != add[mult[i][j]][mult[i][k]]: return False
                    if mult[add[i][j]][k] != add[mult[i][k]][mult[j][k]]: return False
        return True

    try:
        if not is_ring():
            return [False, False, False, False]
            
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            return [False, False, False, False]

        neg = [None] * n
        for i in range(n):
            for j in range(n):
                if add[i][j] == zero:
                    neg[i] = j
                    break
        if any(x is None for x in neg):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: Z is the set of all zero divisors of R
    try:
        Z_computed = set()
        for a in range(n):
            is_zd = False
            for b in range(n):
                if b != zero:
                    if mult[a][b] == zero or mult[b][a] == zero:
                        is_zd = True
                        break
            if is_zd:
                Z_computed.add(a)
        H1 = (Z_set == Z_computed)
    except Exception:
        H1 = False

    # H_2: I is an ideal of R such that I is a subset of Z
    try:
        def is_ideal(S_set):
            if not S_set: return False
            if zero not in S_set: return False
            for x in S_set:
                for y in S_set:
                    if add[x][y] not in S_set:
                        return False
                    if add[x][neg[y]] not in S_set:
                        return False
            for x in S_set:
                for r in range(n):
                    if mult[r][x] not in S_set: return False
                    if mult[x][r] not in S_set: return False
            return True

        H2 = is_ideal(I_set) and I_set.issubset(Z_set)
    except Exception:
        H2 = False

    # H_3: For any ideal J of R strictly containing I, J is not a subset of Z
    try:
        def ideal_generated_by(S):
            gen = set(S)
            while True:
                old_len = len(gen)
                new_gen = set(gen)
                for x in gen:
                    for y in gen:
                        new_gen.add(add[x][y])
                        new_gen.add(add[x][neg[y]])
                for x in gen:
                    for r in range(n):
                        new_gen.add(mult[r][x])
                        new_gen.add(mult[x][r])
                gen = new_gen
                if len(gen) == old_len:
                    break
            return gen

        H3 = True
        for x in range(n):
            if x not in I_set:
                J = ideal_generated_by(I_set | {x})
                if J.issubset(Z_set):
                    H3 = False
                    break
    except Exception:
        H3 = False

    # ¬Q: I is not a prime ideal of R
    try:
        def get_all_ideals():
            principal_ideals = []
            for i in range(n):
                principal_ideals.append(frozenset(ideal_generated_by([i])))
                
            ideals = set(principal_ideals)
            queue = list(ideals)
            
            while queue:
                if len(ideals) > 1000:
                    return []  # Failsafe to prevent infinite loops/memory issues
                curr = queue.pop(0)
                for pi in principal_ideals:
                    nxt_set = set()
                    for a in curr:
                        for b in pi:
                            nxt_set.add(add[a][b])
                    nxt = frozenset(nxt_set)
                    if nxt not in ideals:
                        ideals.add(nxt)
                        queue.append(nxt)
                        
            return [set(id_set) for id_set in ideals]

        def is_prime_ideal(P_set):
            all_ideals = get_all_ideals()
            if not all_ideals:
                return True  # Failsafe triggers returning True, making neg_Q False
            for A in all_ideals:
                for B in all_ideals:
                    ab_in_P = True
                    for a in A:
                        for b in B:
                            if mult[a][b] not in P_set:
                                ab_in_P = False
                                break
                        if not ab_in_P:
                            break
                    if ab_in_P:
                        if not A.issubset(P_set) and not B.issubset(P_set):
                            return False
            return True

        neg_Q = not is_prime_ideal(I_set)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]