import math

# Top-level setup
# No specific named bindings are required for this domain, as witnesses will provide the parameters directly.

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary specifying ideals in Z and a Z-algebra B.
    Format:
    {
        'domain': 'Z',
        'I_gen': a,  # integer, generator of I
        'J_gen': b,  # integer, generator of J
        'B_mod': n   # integer, B = Z/nZ
    }
    """
    try:
        if isinstance(witness, dict) and witness.get('domain') == 'Z':
            a = int(witness['I_gen'])
            b = int(witness['J_gen'])
            n = int(witness['B_mod'])
            
            # H1: R is a commutative ring (Z is commutative)
            h1 = True
            
            # H2: I and J are ideals of A (aZ and bZ are ideals of Z)
            h2 = True
            
            # H3: I + J = A (aZ + bZ = Z iff gcd(a, b) == 1)
            h3 = math.gcd(a, b) == 1
            
            # neg_Q: The extended ideals I \otimes B and J \otimes B are NOT comaximal in A \otimes B.
            # This happens because I \otimes B is not even an ideal IN A \otimes B
            # (the canonical map I \otimes B -> A \otimes B is not injective).
            if n == 0:
                neg_q = False
            else:
                not_inj_I = (a != 0 and math.gcd(a, n) > 1)
                not_inj_J = (b != 0 and math.gcd(b, n) > 1)
                neg_q = not_inj_I or not_inj_J
            
            return [h1, h2, h3, neg_q]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of A",
    "H_3: I + J = A",
    "¬Q: I \\otimes B and J \\otimes B are not ideals in A \\otimes B (canonical maps not injective)"
]

N_HYP = 3
NEG_Q_INDEX = 3