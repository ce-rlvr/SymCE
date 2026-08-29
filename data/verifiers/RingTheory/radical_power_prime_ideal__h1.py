import sympy
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    # Extract P, n, R from the witness
    P, n, R = None, None, None
    is_dict = False
    try:
        if isinstance(witness, dict):
            is_dict = True
            P = witness.get('P')
            n = witness.get('n')
            R = witness.get('R')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                R, P, n = witness
            elif len(witness) == 2:
                P, n = witness
        else:
            P = getattr(witness, 'P', None)
            n = getattr(witness, 'n', None)
            R = getattr(witness, 'R', None)
    except Exception:
        pass

    # Evaluate H_1: P is a prime ideal of R
    try:
        if is_dict and 'is_prime_ideal' in witness:
            h1 = bool(witness['is_prime_ideal'])
        elif hasattr(witness, 'is_prime_ideal'):
            h1 = bool(witness.is_prime_ideal() if callable(witness.is_prime_ideal) else witness.is_prime_ideal)
        elif hasattr(P, 'is_prime_ideal'):
            try:
                h1 = bool(P.is_prime_ideal(R) if callable(P.is_prime_ideal) else P.is_prime_ideal)
            except Exception:
                h1 = bool(P.is_prime_ideal() if callable(P.is_prime_ideal) else P.is_prime_ideal)
        elif hasattr(P, 'is_prime'):
            h1 = bool(P.is_prime() if callable(P.is_prime) else P.is_prime)
        elif isinstance(P, (int, sympy.Integer)):
            h1 = bool(sympy.isprime(P))
    except Exception:
        h1 = False

    # Evaluate H_2: n is a positive integer
    try:
        if is_dict and 'n' in witness:
            n_val = witness['n']
            h2 = isinstance(n_val, int) and n_val > 0
        else:
            h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # Evaluate ¬Q: The radical of the ideal P^n is not equal to P
    try:
        if is_dict and 'radical_equals_P' in witness:
            neg_q = not bool(witness['radical_equals_P'])
        elif hasattr(witness, 'radical_equals_P'):
            rad_eq = witness.radical_equals_P() if callable(witness.radical_equals_P) else witness.radical_equals_P
            neg_q = not bool(rad_eq)
        elif hasattr(witness, 'radical_of_power_equals_P'):
            rad_eq = witness.radical_of_power_equals_P() if callable(witness.radical_of_power_equals_P) else witness.radical_of_power_equals_P
            neg_q = not bool(rad_eq)
        elif P is not None and n is not None and h2:
            Pn = P ** n
            rad_Pn = None
            if hasattr(Pn, 'radical'):
                rad_Pn = Pn.radical() if callable(Pn.radical) else Pn.radical
            elif hasattr(Pn, 'rad'):
                rad_Pn = Pn.rad() if callable(Pn.rad) else Pn.rad
            elif isinstance(P, (int, sympy.Integer)):
                factors = factorint(Pn)
                rad_Pn = 1
                for prime in factors:
                    rad_Pn *= prime
            
            if rad_Pn is not None:
                neg_q = (rad_Pn != P)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: n is a positive integer",
    "¬Q: The radical of the ideal P^n is not equal to P"
]

N_HYP = 2
NEG_Q_INDEX = 2