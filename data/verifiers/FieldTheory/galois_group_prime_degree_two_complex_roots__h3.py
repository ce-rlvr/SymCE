import sympy
from sympy import Symbol, Poly, discriminant, sqrt, factor_list, prime, isprime

x = Symbol('x')

def conditions(witness):
    try:
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 1:
            var = list(witness.free_symbols)[0]
        else:
            var = x
        poly = Poly(witness, var)
        p = poly.degree()
        h1 = isprime(p)
    except Exception:
        h1 = False
        p = 0
        var = x

    try:
        if h1:
            facs = factor_list(witness)
            if len(facs[1]) == 1 and facs[1][0][1] == 1:
                f_fac = facs[1][0][0]
                deg_fac = f_fac.degree() if hasattr(f_fac, 'degree') else Poly(f_fac, var).degree()
                h2 = (deg_fac == p)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            D = discriminant(witness, var)
            if D == 0:
                neg_q = False
            elif sqrt(D).is_Rational:
                # If the discriminant is a perfect square, the Galois group is a subgroup of A_p, so not S_p
                neg_q = True
            elif p == 2:
                # For p=2, any irreducible polynomial has Galois group S_2
                neg_q = False
            elif p == 3:
                # For p=3, the only transitive subgroups are A_3 and S_3. 
                # Since D is not a square, it must be S_3.
                neg_q = False
            else:
                # For p >= 5, we use the theorem that a transitive subgroup of S_p (p prime) 
                # is S_p if and only if it contains a transposition.
                # We search for a transposition by factoring modulo primes.
                try:
                    _, f_int_poly = poly.clear_denoms()
                except Exception:
                    f_int_poly = poly
                
                lc = f_int_poly.coeffs()[0]
                has_transposition = False
                transposition_type = tuple([2] + [1]*(p-2))
                
                primes_checked = 0
                idx = 1
                
                while primes_checked < 2000:
                    q = prime(idx)
                    idx += 1
                    # Skip primes dividing the leading coefficient or the discriminant
                    if lc % q == 0 or D % q == 0:
                        continue
                        
                    try:
                        facs_mod = factor_list(f_int_poly, modulus=q)
                        degs = tuple(sorted([f.degree() if hasattr(f, 'degree') else Poly(f, var).degree() for f, e in facs_mod[1]], reverse=True))
                        
                        if degs == transposition_type:
                            has_transposition = True
                            break
                    except Exception:
                        pass
                        
                    primes_checked += 1
                
                if has_transposition:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Degree of f(x) is a prime number p",
    "H_2: f(x) is irreducible over Q",
    "¬Q: The Galois group of f(x) over Q is not isomorphic to S_p"
]

N_HYP = 2
NEG_Q_INDEX = 2