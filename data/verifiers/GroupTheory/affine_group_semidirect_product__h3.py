import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_prime_power(n):
    if not isinstance(n, int) or n < 2:
        return False
    factors = sympy.ntheory.factorint(n)
    return len(factors) == 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (n, q, phi_type) or dict representing
    a vector space V of dimension n over a field of order q, and an action phi.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
            phi_type = witness.get('phi_type', 'trivial')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, q, phi_type = witness
            elif len(witness) == 2:
                n, q = witness
                phi_type = 'trivial'
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: V is a vector space over a field F
    try:
        h1 = isinstance(n, int) and n >= 1 and is_prime_power(q)
    except Exception:
        h1 = False
        
    # H_2: GL(V) is the general linear group of V
    # This is definitional and holds whenever V is a valid vector space.
    h2 = h1
    
    # ¬Q: Aff(V) is not isomorphic to V ⋊_φ GL(V)
    try:
        if not h1:
            neg_q = False
        else:
            if phi_type == 'trivial':
                # If phi is the trivial action, V ⋊_φ GL(V) is the direct product V x GL(V).
                # We can distinguish Aff(V) and V x GL(V) by the sizes of their centers.
                
                # Center size of Aff(n, q)
                if n == 1 and q == 2:
                    center_aff = 2
                else:
                    center_aff = 1
                
                # Center size of V x GL(n, q)
                # The center of GL(n, q) consists of scalar matrices, so its size is q - 1.
                center_sdp = (q**n) * (q - 1)
                
                neg_q = (center_aff != center_sdp)
            else:
                # For other actions, we default to False unless explicitly evaluated
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: GL(V) is the general linear group of V",
    "¬Q: Aff(V) is not isomorphic to V ⋊_φ GL(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2