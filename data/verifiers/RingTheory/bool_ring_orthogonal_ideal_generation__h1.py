import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
from functools import reduce

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
    N = None
    S = None
    
    try:
        if isinstance(witness, dict) and 'N' in witness and 'S' in witness:
            N = witness['N']
            S = witness['S']
        elif isinstance(witness, tuple) and len(witness) == 2:
            try:
                N_val = int(witness[0])
                S_val = list(witness[1])
                N = N_val
                S = S_val
            except Exception:
                S = list(witness)
        elif isinstance(witness, (list, tuple)):
            S = list(witness)
    except Exception:
        pass

    if N is not None:
        try:
            N = int(N)
            if N < 2:
                N = None
            else:
                S = [int(x) % N for x in S]
        except Exception:
            N = None

    # H1: S is a finite set of elements
    try:
        h1 = isinstance(S, list) and len(S) > 0
        if h1:
            has_duplicates = False
            for i in range(len(S)):
                for j in range(i + 1, len(S)):
                    if S[i] == S[j]:
                        has_duplicates = True
                        break
                if has_duplicates:
                    break
            if has_duplicates:
                h1 = False
    except Exception:
        h1 = False

    # H2: x_i * x_j = 0 for all i != j
    try:
        h2 = True
        if not h1:
            h2 = False
        elif N is not None:
            for i in range(len(S)):
                for j in range(len(S)):
                    if i != j:
                        if (S[i] * S[j]) % N != 0:
                            h2 = False
                            break
                if not h2:
                    break
        else:
            for i in range(len(S)):
                for j in range(len(S)):
                    if i != j:
                        prod = S[i] * S[j]
                        is_zero = False
                        if hasattr(prod, 'is_zero_matrix') and prod.is_zero_matrix:
                            is_zero = True
                        elif hasattr(prod, 'is_zero') and prod.is_zero:
                            is_zero = True
                        elif prod == 0:
                            is_zero = True
                        else:
                            try:
                                from sympy import simplify
                                if simplify(prod) == 0:
                                    is_zero = True
                            except Exception:
                                pass
                        if not is_zero:
                            h2 = False
                            break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: ideal(S) != ideal(sum(S))
    try:
        neg_q = False
        if not h1:
            neg_q = False
        elif N is not None:
            ideal_S = reduce(math.gcd, S + [N])
            ideal_sum = math.gcd(sum(S), N)
            neg_q = (ideal_S != ideal_sum)
        else:
            s_sum = S[0]
            for x in S[1:]:
                s_sum = s_sum + x
                
            is_sum_zero = False
            if hasattr(s_sum, 'is_zero_matrix') and s_sum.is_zero_matrix:
                is_sum_zero = True
            elif hasattr(s_sum, 'is_zero') and s_sum.is_zero:
                is_sum_zero = True
            elif s_sum == 0:
                is_sum_zero = True
            else:
                try:
                    from sympy import simplify
                    if simplify(s_sum) == 0:
                        is_sum_zero = True
                except Exception:
                    pass
                
            has_nonzero = False
            for x in S:
                is_x_zero = False
                if hasattr(x, 'is_zero_matrix') and x.is_zero_matrix:
                    is_x_zero = True
                elif hasattr(x, 'is_zero') and x.is_zero:
                    is_x_zero = True
                elif x == 0:
                    is_x_zero = True
                else:
                    try:
                        from sympy import simplify
                        if simplify(x) == 0:
                            is_x_zero = True
                    except Exception:
                        pass
                if not is_x_zero:
                    has_nonzero = True
                    break
                    
            if is_sum_zero and has_nonzero:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a finite set of elements",
    "H_2: x_i * x_j = 0 for all i != j",
    "¬Q: The ideal generated by S is NOT generated by the sum x_1 + ... + x_n"
]

N_HYP = 2
NEG_Q_INDEX = 2