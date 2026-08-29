import sympy

# Top-level setup: named object bindings that the witness expression may reference.
ZZ = sympy.ZZ
QQ = sympy.QQ

def is_trivial(R):
    """Check if the ring R is the trivial ring (where 1 == 0)."""
    if isinstance(R, str):
        R_clean = R.replace(" ", "")
        return R_clean in ['Z/1Z', 'trivial', '{0}', '0']
    if isinstance(R, int):
        # Using the convention that integer n represents Z/nZ
        return abs(R) == 1
    if R in [sympy.ZZ, sympy.QQ]:
        return False
    if hasattr(R, 'zero') and hasattr(R, 'one'):
        return R.zero == R.one
    return False

def is_commutative_ring(R):
    """Check if R is a commutative ring."""
    if isinstance(R, str):
        return True
    if isinstance(R, int):
        return True
    if R in [sympy.ZZ, sympy.QQ]:
        return True
    if hasattr(R, 'is_commutative'):
        return R.is_commutative
    return True  # Fallback assumption for unknown objects

def is_euclidean_domain(R):
    """Check if R is a Euclidean domain."""
    if is_trivial(R):
        return False
    if isinstance(R, str):
        R_clean = R.replace(" ", "")
        if R_clean in ['Z', 'QQ', 'ZZ', 'Q', 'R', 'C']:
            return True
        if R_clean.startswith('Z/') and R_clean.endswith('Z'):
            try:
                n = int(R_clean[2:-1])
                return sympy.isprime(n)
            except ValueError:
                return False
        return False
    if isinstance(R, int):
        # Z/nZ is a Euclidean domain iff it is a field (n is prime) or Z (n = 0)
        return R == 0 or sympy.isprime(abs(R))
    if R in [sympy.ZZ, sympy.QQ]:
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        # Polynomial ring over a field in one variable is a Euclidean domain
        if len(R.symbols) == 1 and getattr(R.domain, 'is_Field', False):
            return True
    return False

def is_euclidean_domain_product(R1, R2):
    """
    A direct product of two rings R1 x R2 is a Euclidean domain if and only if 
    one of the rings is trivial and the other is a Euclidean domain.
    (Since a Euclidean domain must be an integral domain, and a product has zero divisors 
    unless one factor is trivial).
    """
    t1 = is_trivial(R1)
    t2 = is_trivial(R2)
    if t1 and not t2:
        return is_euclidean_domain(R2)
    if t2 and not t1:
        return is_euclidean_domain(R1)
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        R1, R2 = witness
        
        # H_1: R_2 is a non-trivial commutative ring
        h1_ok = bool(is_commutative_ring(R2) and not is_trivial(R2))
        
        # neg_Q: The direct product R_1 x R_2 IS a Euclidean domain
        neg_q_ok = bool(is_euclidean_domain_product(R1, R2))
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R_2 is a non-trivial commutative ring",
    "¬Q: The direct product R_1 x R_2 is a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1