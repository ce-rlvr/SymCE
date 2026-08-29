import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.ntheory import isprime

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            k = witness.get('k')
            n = witness.get('n')
            N = witness.get('N')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            k, n, N = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: k is an odd positive integer
    try:
        h1 = isinstance(k, int) and not isinstance(k, bool) and k > 0 and k % 2 == 1
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h2 = False

    # H3: k < 2^n
    try:
        h3 = isinstance(k, int) and isinstance(n, int) and k < (2 ** n)
    except Exception:
        h3 = False

    # neg_Q: N is prime iff exists a such that a^{(N-1)/2} == -1 mod N
    try:
        if not isinstance(N, int) or isinstance(N, bool) or N <= 0:
            neg_q = False
        else:
            is_p = isprime(N)
            
            exists_a = False
            if N % 2 == 1:
                power = (N - 1) // 2
                # Check N - 1 first as it's a common solution for composite N = 3 mod 4
                if pow(N - 1, power, N) == N - 1:
                    exists_a = True
                else:
                    # Bounded search to ensure fast execution
                    for a in range(1, min(N, 10000)):
                        if pow(a, power, N) == N - 1:
                            exists_a = True
                            break
            
            q_holds = exists_a
            
            # The conclusion is: is_p <-> q_holds
            # We want the negation of the conclusion, so is_p != q_holds
            neg_q = (is_p != q_holds)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: k is an odd positive integer",
    "H_2: n is a positive integer",
    "H_3: k < 2^n",
    "¬Q: N is not (prime iff exists a such that a^{(N-1)/2} == -1 mod N)"
]

N_HYP = 3
NEG_Q_INDEX = 3