import sympy
from sympy import Poly, discriminant, integer_nthroot
from sympy.abc import x
from sympy.ntheory import isprime, primerange

# Top-level setup
# The witness is expected to be a polynomial expression in x.

def conditions(witness):
    try:
        f = Poly(witness, x, domain='QQ')
    except Exception:
        return [False, False, False, False]
    
    # H_1: f is a polynomial over Q
    h1 = True
    
    # H_2: f is irreducible over Q
    try:
        h2 = f.is_irreducible
    except Exception:
        h2 = False
        
    # H_3: The degree of f is a prime number
    try:
        p = f.degree()
        h3 = isprime(p)
    except Exception:
        h3 = False
        
    # ¬Q: The Galois group of f over Q is NOT isomorphic to S_p
    neg_q = False
    try:
        if h2 and h3:
            if p == 2:
                # For p=2, the Galois group of an irreducible quadratic is always S_2.
                neg_q = False
            else:
                disc = discriminant(f.as_expr(), x)
                
                # Check if the discriminant is a perfect square in Q.
                # If it is, the Galois group is a subgroup of A_p, so it cannot be S_p.
                if disc.is_Rational:
                    if disc < 0:
                        is_sq = False
                    else:
                        num = abs(disc.p)
                        den = disc.q
                        root_num, exact_num = integer_nthroot(num, 2)
                        root_den, exact_den = integer_nthroot(den, 2)
                        is_sq = exact_num and exact_den
                else:
                    is_sq = False
                
                if is_sq:
                    neg_q = True
                elif p == 3:
                    # For p=3, the only transitive subgroup of S_3 not in A_3 is S_3 itself.
                    # Since the discriminant is not a square, it must be S_3.
                    neg_q = False
                else:
                    # For prime p >= 5, the only primitive groups not contained in A_p 
                    # are S_p and subgroups of the affine group AGL(1, p) (and a few rare exceptions).
                    # AGL(1, p) has no non-identity elements with >= 2 fixed points.
                    # S_p has elements with >= 2 fixed points (e.g., 3-cycles have p-3 >= 2 fixed points).
                    # We factor f(x) modulo primes to find the cycle types of the Frobenius elements.
                    found_multiple_roots = False
                    count = 0
                    f_int = f.clear_denoms()[1]
                    
                    for q in primerange(2, 2000):
                        if count >= 150:
                            break
                        
                        # Skip primes that divide the leading coefficient or the discriminant
                        if f_int.LC() % q == 0:
                            continue
                        if disc.is_Rational and (disc.p % q == 0 or disc.q % q == 0):
                            continue
                        
                        try:
                            factors = sympy.factor_list(f_int.as_expr(), modulus=q)[1]
                        except Exception:
                            continue
                        
                        # Count the number of linear factors (fixed points of the permutation)
                        linear_factors = sum(mult for factor, mult in factors if sympy.degree(factor, x) == 1)
                        
                        # If we find an element with >= 2 fixed points (and not the identity which has p),
                        # the group cannot be a subgroup of AGL(1, p). Thus it is likely S_p.
                        if 2 <= linear_factors < p:
                            found_multiple_roots = True
                            break
                        
                        count += 1
                    
                    if found_multiple_roots:
                        neg_q = False  # It is S_p
                    else:
                        neg_q = True   # It is a subgroup of AGL(1, p), so NOT S_p
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Q",
    "H_2: f is irreducible over Q",
    "H_3: The degree of f is a prime number",
    "¬Q: The Galois group of f over Q is NOT isomorphic to S_p"
]

N_HYP = 3
NEG_Q_INDEX = 3