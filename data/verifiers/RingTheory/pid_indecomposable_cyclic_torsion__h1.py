import sympy
import itertools
from sympy.abc import x, y, z, t, u, v, w
from sympy import QQ, ZZ
from sympy.ntheory import factorint

# Top-level setup
# No specific named objects required for this ring theory theorem,
# but standard symbols and domains are available for witness expressions.

def conditions(witness) -> list[bool]:
    try:
        domain = None
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            domain, a = witness
        else:
            a = witness

        a = sympy.sympify(a)
    except Exception:
        return [False, False, False]

    try:
        domain_str = str(domain) if domain is not None else ""
        if 'QQ' in domain_str or 'Q' in domain_str or 'Field' in domain_str:
            base_ring = 'QQ'
        else:
            base_ring = 'ZZ'

        symbols = list(a.free_symbols)
    except Exception:
        return [False, False, False]

    # H1: a is a non-zero element of R
    try:
        h1 = bool(a != 0)
    except Exception:
        h1 = False

    # H2: a is not a unit in R
    try:
        if a == 0:
            is_u = False
        elif not symbols:
            if base_ring == 'QQ':
                is_u = True
            else:
                is_u = bool(abs(a) == 1)
        else:
            is_u = False
        h2 = not is_u
    except Exception:
        h2 = False

    # Conclusion: R/(a) is indecomposable if and only if a = p^k u
    try:
        if a == 0 or is_u:
            # If a is 0 or a unit, the theorem's context is violated, 
            # but we evaluate the biconditional strictly.
            neg_q = True
        else:
            coeff, factors = sympy.factor_list(a, domain=base_ring)
            primes = []
            
            if base_ring == 'ZZ':
                if abs(coeff) > 1:
                    for p, k in factorint(abs(coeff)).items():
                        primes.append((sympy.Integer(p), k))
            
            for base, exp in factors:
                primes.append((base, exp))
            
            # Right side of biconditional: a = p^k u
            is_pk_u = (len(primes) == 1)
            
            # Left side of biconditional: R/(a) is indecomposable
            if len(primes) <= 1:
                is_indecomp = True
            else:
                is_indecomp = True
                indices = list(range(len(primes)))
                # Check all partitions of prime factors into two non-empty sets B and C
                for r in range(1, len(primes)):
                    for subset in itertools.combinations(indices, r):
                        b = sympy.Integer(1)
                        c = sympy.Integer(1)
                        for i in indices:
                            if i in subset:
                                b *= primes[i][0]**primes[i][1]
                            else:
                                c *= primes[i][0]**primes[i][1]
                        
                        if not symbols:
                            # Over ZZ, 1 in (b, c) iff gcd(b, c) == 1
                            if sympy.gcd(b, c) == 1:
                                is_indecomp = False
                                break
                        else:
                            # Over polynomial rings, 1 in (b, c) iff Groebner basis is [1]
                            gb = sympy.groebner([b, c], *symbols, domain=base_ring)
                            gb_list = list(gb)
                            if gb_list == [1] or gb_list == [-1]:
                                is_indecomp = False
                                break
                    if not is_indecomp:
                        break
            
            conclusion = (is_indecomp == is_pk_u)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is a non-zero element of R",
    "H_2: a is not a unit in R",
    "¬Q: The equivalence between R/(a) being indecomposable and a = p^k u fails"
]

N_HYP = 2
NEG_Q_INDEX = 2