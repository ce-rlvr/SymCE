import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: P is a prime ideal of R",
    "¬Q: P does not contain any prime element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        # Witness can be a list of generators (assuming ZZ) or a tuple (domain, generators)
        if isinstance(witness, list):
            domain = ZZ
            gens = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            domain, gens = witness
        else:
            return [False, False, False]
            
        # Map basic SymPy sets to poly domains if provided
        if domain == sympy.S.Integers:
            domain = ZZ
        elif domain == sympy.S.Rationals:
            domain = QQ

        # H1: R is a UFD
        try:
            h1 = bool(getattr(domain, 'is_UFD', False))
        except Exception:
            h1 = False
            
        # H2: P is a prime ideal of R
        try:
            valid_gens = [domain.convert(g) for g in gens]
            is_zero = all(g == domain.zero for g in valid_gens)
            
            if is_zero:
                # The zero ideal is prime in any integral domain (all UFDs are integral domains)
                h2 = h1 
            else:
                if getattr(domain, 'is_PID', False):
                    g = valid_gens[0]
                    for e in valid_gens[1:]:
                        g = domain.gcd(g, e)
                    
                    if g == domain.zero:
                        h2 = True
                    elif domain == ZZ:
                        h2 = sympy.isprime(abs(int(g)))
                    elif hasattr(domain, 'is_irreducible'):
                        h2 = domain.is_irreducible(g)
                    else:
                        h2 = False
                else:
                    # For non-PIDs, we only reliably check the zero ideal in this verifier
                    h2 = False
        except Exception:
            h2 = False
            
        # neg_Q: P does NOT contain a prime element of R
        try:
            valid_gens = [domain.convert(g) for g in gens]
            is_zero = all(g == domain.zero for g in valid_gens)
            
            if is_zero:
                # The zero ideal contains only 0, which is not a prime element
                neg_q = True
            elif getattr(domain, 'is_Field', False):
                # Fields have no prime elements
                neg_q = True
            elif getattr(domain, 'is_PID', False):
                g = valid_gens[0]
                for e in valid_gens[1:]:
                    g = domain.gcd(g, e)
                
                if g == domain.zero:
                    neg_q = True
                elif domain == ZZ:
                    val = abs(int(g))
                    # In ZZ, ideal (g) contains a prime iff g is 1 or prime
                    contains_prime = (val == 1 or sympy.isprime(val))
                    neg_q = not contains_prime
                else:
                    # In other PIDs, ideal (g) contains a prime iff g is a unit or irreducible
                    if hasattr(domain, 'is_unit') and domain.is_unit(g):
                        neg_q = False
                    elif hasattr(domain, 'is_irreducible') and domain.is_irreducible(g):
                        neg_q = False
                    else:
                        neg_q = True
            else:
                # Fallback for non-PIDs: check if any generator is prime
                contains_prime = False
                for g in valid_gens:
                    if domain == ZZ:
                        if sympy.isprime(abs(int(g))):
                            contains_prime = True
                            break
                    elif hasattr(domain, 'is_irreducible') and domain.is_irreducible(g):
                        contains_prime = True
                        break
                neg_q = not contains_prime
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]