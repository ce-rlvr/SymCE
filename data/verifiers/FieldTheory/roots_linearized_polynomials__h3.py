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
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: L(x) is a linearized polynomial with coefficients in F_{q^m}",
    "¬Q: The set of roots of L(x) in E does not form a vector space over F_q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        q = witness[0]
        m = witness[1]
        a_list = witness[2]
        E = witness[3]
    except Exception:
        return [False, False, False]
        
    # H1: F_q is a finite field (q must be a prime power)
    try:
        h1 = bool(sympy.ntheory.is_primepower(q))
    except Exception:
        h1 = False
        
    # H2: L(x) is a linearized polynomial with coefficients in F_{q^m}
    try:
        h2 = False
        if isinstance(m, int) and m >= 1:
            if isinstance(a_list, (list, tuple)):
                # Verify all coefficients can be interpreted as elements of the prime subfield
                _ = [int(a) for a in a_list]
                h2 = True
    except Exception:
        h2 = False
        
    # Negated Conclusion: The set of roots of L(x) in E does NOT form a vector space over F_q
    try:
        neg_q_cond = False
        if h1 and h2:
            factors = sympy.ntheory.factorint(q)
            p = list(factors.keys())[0]
            
            # Evaluate L(x) = sum(a_i * x^{q^i}) for x in E.
            # We map elements of E to the prime subfield F_p.
            # By Fermat's Little Theorem, for x in F_p, x^q = x^{p^k} = x mod p.
            # Thus, L(x) = sum(a_i * x) = (sum a_i) * x mod p.
            sum_a = sum(int(a) for a in a_list) % p
            
            R_mod = set()
            for x in E:
                x_int = int(x)
                if (sum_a * x_int) % p == 0:
                    R_mod.add(x_int % p)
            
            is_vs = True
            if q == p:
                # Check if R_mod is a vector space over F_p
                if 0 not in R_mod:
                    is_vs = False
                else:
                    for x in R_mod:
                        for y in R_mod:
                            if (x + y) % p not in R_mod:
                                is_vs = False
                                break
                        if not is_vs:
                            break
                    if is_vs:
                        for c in range(p):
                            for x in R_mod:
                                if (c * x) % p not in R_mod:
                                    is_vs = False
                                    break
                            if not is_vs:
                                break
            else:
                # If q > p, a subset of F_p can only be a vector space over F_q if it is {0}
                if R_mod != {0}:
                    is_vs = False
                else:
                    is_vs = True
                    
            neg_q_cond = not is_vs
    except Exception:
        neg_q_cond = False
        
    return [h1, h2, neg_q_cond]