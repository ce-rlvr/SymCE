import sympy as sp
import math
from itertools import combinations
from sympy.ntheory import factorint
from sympy import eye, zeros

# Expected witness format:
# A tuple (n, A) where n is an integer >= 2 representing the ring Z/nZ,
# and A is a list of lists (or a SymPy Matrix) representing the presentation
# matrix of the module M over Z/nZ.
# Example counterexample: witness = (6, [[3]])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elementary_divisors(A):
    m, k = A.shape
    if m == 0 or k == 0:
        return []
    
    # For larger matrices, try to use SymPy's smith_normal_form
    if m > 6 or k > 6:
        try:
            from sympy.matrices.normalforms import smith_normal_form
            S = smith_normal_form(A)
            return [S[j, j] for j in range(min(m, k))]
        except ImportError:
            if m > 8 or k > 8:
                return None
            
    # For smaller matrices, compute elementary divisors via GCD of minors
    minors_gcd = []
    for i in range(1, min(m, k) + 1):
        current_gcd = 0
        for rows in combinations(range(m), i):
            for cols in combinations(range(k), i):
                minor = A[list(rows), list(cols)].det()
                current_gcd = math.gcd(current_gcd, int(minor))
                if current_gcd == 1:
                    break
            if current_gcd == 1:
                break
        minors_gcd.append(current_gcd)
        
    edivs = []
    D_prev = 1
    for D in minors_gcd:
        if D == 0:
            edivs.append(0)
        else:
            edivs.append(D // D_prev)
            D_prev = D
    return edivs

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            A_raw = witness.get('A', [])
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, A_raw = witness
            n = int(n)
        else:
            return [False, False, False]
            
        if n < 2:
            return [False, False, False]
            
        A = sp.Matrix(A_raw)
        for x in A:
            if not x.is_integer:
                return [False, False, False]
                
        m, k = A.shape
        
        # H_1: M is a finitely generated R-module
        # Since M is presented by a finite matrix A over Z/nZ, it is finitely generated.
        H1_ok = True
        
        edivs = get_elementary_divisors(A)
        if edivs is None:
            return [False, False, False]
            
        factors = factorint(n)
        
        is_flat = True
        ranks = []
        
        # Check flatness and compute local ranks
        for p, e in factors.items():
            pe = p ** e
            c_p = 0
            for d in edivs:
                d_mod = d % pe
                if math.gcd(d_mod, p) == 1:
                    c_p += 1
                elif d_mod == 0:
                    pass
                else:
                    is_flat = False
                    break
            if not is_flat:
                break
            # The rank of the free module over the local component Z/p^e Z
            ranks.append(m - c_p)
            
        # H_2: M is a flat R-module
        H2_ok = is_flat
        
        # ¬Q: M is not a free R-module
        if not is_flat:
            neg_Q_ok = False
        else:
            # M is free over Z/nZ iff it is flat and has the same rank at all localizations
            is_free = (len(set(ranks)) <= 1)
            neg_Q_ok = not is_free
            
        return [H1_ok, H2_ok, neg_Q_ok]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: M is a flat R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2