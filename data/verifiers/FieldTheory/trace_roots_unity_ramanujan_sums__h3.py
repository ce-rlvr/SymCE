import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import math

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

def conditions(witness) -> list[bool]:
    # witness is expected to be a tuple (n, k, zeta_n)
    if isinstance(witness, dict):
        n = witness.get('n')
        k = witness.get('k')
        zeta_n = witness.get('zeta_n')
    else:
        try:
            n, k, zeta_n = witness
        except Exception:
            return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: zeta_n is a primitive n-th root of unity
    try:
        if not h1:
            h2 = False
        else:
            val1 = sympy.simplify(zeta_n**n - 1)
            if val1 != 0:
                h2 = False
            else:
                h2 = True
                for p in sympy.ntheory.primefactors(n):
                    if sympy.simplify(zeta_n**(n // p) - 1) == 0:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: The field trace is NOT equal to the Ramanujan sum
    neg_q = False
    try:
        if h1 and h2:
            # Compute the field trace: Tr(zeta_n^k) = sum_{gcd(m,n)=1} zeta_n^{k*m}
            trace_val = 0
            for m in range(1, n + 1):
                if math.gcd(m, n) == 1:
                    trace_val += zeta_n**(k * m)
            trace_val = sympy.simplify(trace_val)
            
            try:
                k_sym = sympy.sympify(k)
                n_sym = sympy.sympify(n)
                g = sympy.gcd(k_sym, n_sym)
                
                # If gcd(k, n) is not an integer, the Ramanujan sum is undefined over integers,
                # hence the equality with the trace fails.
                if not g.is_Integer:
                    neg_q = True
                else:
                    # Compute the Ramanujan sum: sum_{d | gcd(k,n)} d * mu(n/d)
                    ram_sum = 0
                    for d in sympy.ntheory.divisors(int(g)):
                        if d > 0:
                            ram_sum += d * sympy.ntheory.mobius(n // d)
                    
                    diff = sympy.simplify(trace_val - ram_sum)
                    neg_q = (diff != 0)
            except Exception:
                # If Ramanujan sum computation fails (e.g., due to non-integer k), equality fails
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: zeta_n is a primitive n-th root of unity",
    "¬Q: The field trace is not equal to the Ramanujan sum"
]

N_HYP = 2
NEG_Q_INDEX = 2