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
    n = None
    zeta_n = None
    tau = None
    
    if isinstance(witness, dict):
        n = witness.get('n')
        zeta_n = witness.get('zeta_n')
        tau = witness.get('tau')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            n, zeta_n, tau = witness
        elif len(witness) == 2:
            n, tau = witness
    else:
        n = witness

    # H_1: n is an integer with n >= 3
    try:
        if isinstance(n, sympy.Integer):
            n = int(n)
        elif isinstance(n, float) and n.is_integer():
            n = int(n)
        h1 = isinstance(n, int) and n >= 3
    except Exception:
        h1 = False

    if zeta_n is None and h1:
        try:
            zeta_n = sympy.exp(2 * sympy.pi * sympy.I / n)
        except Exception:
            pass

    # H_2: zeta_n is a primitive n-th root of unity in C
    try:
        h2 = False
        if h1 and zeta_n is not None:
            val = complex(zeta_n)
            if abs(val**n - 1) < 1e-7:
                h2 = True
                for d in range(1, n // 2 + 1):
                    if n % d == 0:
                        if abs(val**d - 1) < 1e-7:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # ¬Q: The restriction of tau to Q(zeta_n) is not a non-trivial Galois automorphism of order 2 that maps zeta_n to zeta_n^-1
    try:
        Q = False
        if h1 and h2 and tau is not None:
            if isinstance(tau, (int, sympy.Integer)):
                k = int(tau)
                n_int = int(n)
                is_galois = (math.gcd(abs(k), n_int) == 1)
                is_order_2 = (k**2 % n_int == 1) and (k % n_int != 1)
                maps_to_inv = (k % n_int == (-1) % n_int)
                Q = is_galois and is_order_2 and maps_to_inv
            elif callable(tau):
                tz = tau(zeta_n)
                ttz = tau(tz)
                val_z = complex(zeta_n)
                val_tz = complex(tz)
                val_ttz = complex(ttz)
                
                is_galois = False
                if abs(val_tz**n - 1) < 1e-7:
                    is_galois = True
                    for d in range(1, n // 2 + 1):
                        if n % d == 0:
                            if abs(val_tz**d - 1) < 1e-7:
                                is_galois = False
                                break
                is_order_2 = (abs(val_ttz - val_z) < 1e-7) and (abs(val_tz - val_z) > 1e-7)
                maps_to_inv = (abs(val_tz - val_z**(-1)) < 1e-7)
                Q = is_galois and is_order_2 and maps_to_inv
            elif hasattr(tau, 'subs') and len(tau.free_symbols) == 1:
                sym = list(tau.free_symbols)[0]
                tz = tau.subs(sym, zeta_n)
                ttz = tau.subs(sym, tz)
                val_z = complex(zeta_n)
                val_tz = complex(tz)
                val_ttz = complex(ttz)
                
                is_galois = False
                if abs(val_tz**n - 1) < 1e-7:
                    is_galois = True
                    for d in range(1, n // 2 + 1):
                        if n % d == 0:
                            if abs(val_tz**d - 1) < 1e-7:
                                is_galois = False
                                break
                is_order_2 = (abs(val_ttz - val_z) < 1e-7) and (abs(val_tz - val_z) > 1e-7)
                maps_to_inv = (abs(val_tz - val_z**(-1)) < 1e-7)
                Q = is_galois and is_order_2 and maps_to_inv
        
        neg_q = not Q
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 3",
    "H_2: zeta_n is a primitive n-th root of unity in C",
    "¬Q: The restriction of tau to Q(zeta_n) is not a non-trivial Galois automorphism of order 2 that maps zeta_n to zeta_n^-1"
]

N_HYP = 2
NEG_Q_INDEX = 2