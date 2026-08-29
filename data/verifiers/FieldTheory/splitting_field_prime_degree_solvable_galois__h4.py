import sympy
from sympy import Poly, sympify, Symbol
from sympy.ntheory import isprime, nextprime

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    # H1: f(x) is a polynomial over Q (characteristic 0)
    h1 = False
    try:
        if isinstance(witness, Poly):
            p_poly = witness
            if p_poly.domain.is_QQ or p_poly.domain.is_ZZ:
                p_poly = p_poly.set_domain('QQ')
                h1 = True
                gen_x = p_poly.gen
            else:
                h1 = False
        else:
            witness_expr = sympify(witness)
            free_syms = list(witness_expr.free_symbols)
            if len(free_syms) == 1:
                gen_x = free_syms[0]
                p_poly = Poly(witness_expr, gen_x, domain='QQ')
                h1 = True
            elif len(free_syms) == 0:
                gen_x = Symbol('x')
                p_poly = Poly(witness_expr, gen_x, domain='QQ')
                h1 = True
    except Exception:
        h1 = False

    # H2: f(x) is irreducible over Q
    h2 = False
    if h1:
        try:
            h2 = bool(p_poly.is_irreducible)
        except Exception:
            h2 = False

    # H3: The degree of f(x) is a prime number p
    h3 = False
    if h1:
        try:
            deg = p_poly.degree()
            h3 = bool(isprime(deg))
        except Exception:
            h3 = False

    # ¬Q: Two distinct roots do not generate the splitting field.
    # By Galois theory, for a prime degree irreducible polynomial, two roots generate 
    # the splitting field if and only if the Galois group is solvable (i.e. a subgroup of AGL(1, p)).
    # We check for non-solvability by looking for cycle types (factorization degrees mod q)
    # that are forbidden in AGL(1, p).
    neg_q = False
    if h1 and h3:
        try:
            deg = p_poly.degree()
            if deg >= 5:
                # Clear denominators to safely reduce modulo primes
                p_Z = p_poly.clear_denoms()[1]
                primes_checked = 0
                attempts = 0
                q = 2
                
                while primes_checked < 100 and attempts < 1000:
                    attempts += 1
                    
                    # Skip primes dividing the leading coefficient
                    if p_Z.LC() % q == 0:
                        q = nextprime(q)
                        continue
                    
                    try:
                        fp = Poly(p_Z, gen_x, modulus=q)
                        factors = fp.factor_list()
                    except Exception:
                        q = nextprime(q)
                        continue
                    
                    # Skip ramified primes (where the polynomial has repeated roots mod q)
                    multiplicities = [m for _, m in factors[1]]
                    if any(m > 1 for m in multiplicities):
                        q = nextprime(q)
                        continue
                    
                    # Get the degrees of the irreducible factors mod q
                    degrees = sorted([fac.degree() for fac, _ in factors[1]], reverse=True)
                    
                    # Check if the cycle type is allowed in AGL(1, p)
                    # Allowed types: [p], [1, ..., 1], or [k, ..., k, 1] for some k > 1
                    allowed = False
                    if degrees == [deg]:
                        allowed = True
                    elif degrees == [1] * deg:
                        allowed = True
                    elif degrees[-1] == 1 and len(degrees) > 1:
                        k = degrees[0]
                        if all(d == k for d in degrees[:-1]):
                            allowed = True
                            
                    # If we find a forbidden cycle type, the Galois group is not solvable
                    if not allowed:
                        neg_q = True
                        break
                    
                    primes_checked += 1
                    q = nextprime(q)
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q (characteristic 0)",
    "H_2: f(x) is irreducible over Q",
    "H_3: The degree of f(x) is a prime number p",
    "¬Q: Two distinct roots do not generate the splitting field (Galois group is not solvable)"
]

N_HYP = 3
NEG_Q_INDEX = 3