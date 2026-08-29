import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup
from sympy.matrices import eye
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
Z2 = CyclicGroup(2)
I2 = eye(2)

def is_prime_power(n):
    if not isinstance(n, int) or n <= 1:
        return False
    factors = factorint(n)
    return len(factors) == 1

def is_extension(size_E, size_F):
    if not is_prime_power(size_E) or not is_prime_power(size_F):
        return False
    if size_E < size_F:
        return False
    p_E, e_E = list(factorint(size_E).items())[0]
    p_F, e_F = list(factorint(size_F).items())[0]
    return p_E == p_F and e_E % e_F == 0

def conditions(witness):
    """
    Expected witness format:
    A tuple or list (q, K_size, L_size, alpha) or a dictionary with these keys, where:
      - q: size of the finite field F_q
      - K_size: size of the finite field K
      - L_size: size of the finite field L
      - alpha: an integer representing an element of L 
               (0 for the zero element, 1 to L_size-1 for powers of a primitive element)
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            K_size = witness.get('K_size')
            L_size = witness.get('L_size')
            alpha = witness.get('alpha')
        else:
            q, K_size, L_size, alpha = witness
            
        q = int(q)
        K_size = int(K_size)
        L_size = int(L_size)
        alpha = int(alpha)
    except Exception:
        return [False, False, False, False]

    # H1: F_q is a finite field with q elements
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False

    # H2: K is a finite field extension of F_q
    try:
        h2 = is_extension(K_size, q)
    except Exception:
        h2 = False

    # H3: alpha is an element of L
    try:
        h3 = is_prime_power(L_size) and 0 <= alpha < L_size
    except Exception:
        h3 = False

    # Conclusion: N_{L/F_q}(alpha) = N_{K/F_q}(N_{L/K}(alpha))
    try:
        # The conclusion holds if all norm maps are well-defined and the values match.
        # If any norm map is undefined (i.e., the field is not a valid extension), the conclusion fails.
        if not is_extension(L_size, q) or not is_extension(K_size, q) or not is_extension(L_size, K_size):
            c_holds = False
        else:
            if alpha == 0:
                c_holds = True
            else:
                # Using discrete logarithms to compute the norm map.
                # N_{E/F}(g^k) = (g')^{k mod (|F|-1)} where g' is a primitive element of F.
                lhs = alpha % (q - 1)
                inner = alpha % (K_size - 1)
                rhs = inner % (q - 1)
                c_holds = (lhs == rhs)
        neg_q = not c_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: K is a finite field extension of F_q",
    "H_3: alpha is an element of L",
    "not Q: N_{L/F_q}(alpha) != N_{K/F_q}(N_{L/K}(alpha)) or norm map undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3