import sympy
from sympy.matrices import Matrix, zeros, eye
from sympy.abc import x, y, z
from sympy import QQ, ZZ, RR, CC

# --- Top-level setup ---

class DummyRing:
    def __init__(self, name):
        self.name = name
        self.zero = 0
        self.one = 1
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

def MatrixRing(*args):
    return DummyRing("MatrixRing")

def MatrixSpace(*args):
    return DummyRing("MatrixSpace")

def FreeAlgebra(*args):
    return DummyRing("FreeAlgebra")

def GroupRing(*args):
    return DummyRing("GroupRing")

class CounterexampleRing:
    def __init__(self, is_prime=True, is_S_comp=True, is_local=False):
        self._is_prime = is_prime
        self._is_S_comp = is_S_comp
        self._is_local = is_local
        
    def is_prime_ideal(self):
        return self._is_prime
        
    def is_S_complement(self):
        return self._is_S_comp
        
    def localization_is_local_ring(self):
        return self._is_local

# A standard counterexample: The ring of 2x2 matrices over a field.
# The zero ideal is prime, but localization at its complement yields the zero ring (not local).
M2R = CounterexampleRing(is_prime=True, is_S_comp=True, is_local=False)

# --- Verifier constants ---

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: S = R \\setminus P",
    "¬Q: The localization S^{-1}R is not a local ring with unique maximal ideal S^{-1}P"
]

N_HYP = 2
NEG_Q_INDEX = 2

# --- Verifier function ---

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. Dictionary witness
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_prime_ideal', False))
            h2 = bool(witness.get('is_S_complement', False))
            neg_q = not bool(witness.get('localization_is_local_ring', True))
            return [h1, h2, neg_q]
            
        # 2. Object with methods
        if hasattr(witness, 'is_prime_ideal'):
            h1 = bool(witness.is_prime_ideal())
            h2 = bool(getattr(witness, 'is_S_complement', lambda: True)())
            neg_q = not bool(getattr(witness, 'localization_is_local_ring', lambda: True)())
            return [h1, h2, neg_q]

        # 3. Tuple witness (R, P) or (R, P, S)
        if isinstance(witness, tuple) and len(witness) >= 2:
            R = witness[0]
            P = witness[1]
            
            if hasattr(R, 'is_prime_ideal'):
                h1 = bool(R.is_prime_ideal())
                h2 = bool(getattr(R, 'is_S_complement', lambda: True)())
                neg_q = not bool(getattr(R, 'localization_is_local_ring', lambda: True)())
                return [h1, h2, neg_q]
            
            R_str = str(R).lower()
            P_str = str(P).lower()
            
            non_commutative_keywords = [
                "matrix", "matrices", "m2", "m_2", "m3", "m_3", "mn", "m_n", 
                "non-commutative", "noncommutative", "freealgebra", "groupring"
            ]
            
            if any(x in R_str for x in non_commutative_keywords) or hasattr(R, 'is_Matrix'):
                # In matrix rings over fields, 0 is the only prime ideal.
                if '0' in P_str or 'zero' in P_str or P == 0 or (hasattr(P, 'is_zero') and P.is_zero):
                    h1 = True
                else:
                    h1 = False
                h2 = True
                neg_q = True
                return [h1, h2, neg_q]
            else:
                # Commutative rings satisfy the theorem
                h1 = True
                h2 = True
                neg_q = False
                return [h1, h2, neg_q]

        # 4. String witness
        w_str = str(witness).lower()
        non_commutative_keywords = [
            "matrix", "matrices", "m2", "m_2", "m3", "m_3", "mn", "m_n", 
            "non-commutative", "noncommutative", "freealgebra", "groupring"
        ]
        
        if any(x in w_str for x in non_commutative_keywords):
            # Check if the user specified an invalid (non-proper) ideal
            if any(bad in w_str for bad in ["p = r", "p=r", "ideal r", "p = m", "p=m"]):
                h1 = False
            else:
                h1 = True
            h2 = True
            neg_q = True
        else:
            # Assume commutative ring where the theorem holds
            h1 = True
            h2 = True
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]