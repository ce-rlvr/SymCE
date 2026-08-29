import sympy
from sympy.polys.domains import QQ, ZZ, GF, FractionField, AlgebraicField
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # 1. Try as a dictionary
    try:
        if isinstance(witness, dict):
            if 'P' in witness and 'K' in witness and 'K_bar' in witness:
                P = witness['P']
                K = witness['K']
                K_bar = witness['K_bar']
                
                if callable(getattr(K, 'prime_subfield', None)):
                    h1 = (P == K.prime_subfield())
                elif hasattr(K, 'prime_subfield'):
                    h1 = (P == K.prime_subfield)
                elif callable(getattr(P, 'is_prime_subfield_of', None)):
                    h1 = P.is_prime_subfield_of(K)
                    
                if callable(getattr(K_bar, 'is_algebraic_closure_of', None)):
                    h2 = K_bar.is_algebraic_closure_of(K)
                elif hasattr(K, 'algebraic_closure'):
                    h2 = (K_bar == K.algebraic_closure)
                    
                if callable(getattr(K_bar, 'trdeg', None)) and callable(getattr(K, 'trdeg', None)):
                    neg_q = (K_bar.trdeg(P) != K.trdeg(P))
                elif hasattr(K_bar, 'trdeg') and hasattr(K, 'trdeg'):
                    neg_q = (K_bar.trdeg != K.trdeg)
            else:
                h1 = bool(witness.get('H1', witness.get('h1', False)))
                h2 = bool(witness.get('H2', witness.get('h2', False)))
                neg_q = bool(witness.get('neg_Q', witness.get('neg_q', False)))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try as an object with boolean attributes
    try:
        if hasattr(witness, 'P_is_prime_subfield_of_K'):
            h1 = bool(witness.P_is_prime_subfield_of_K)
            h2 = bool(witness.K_bar_is_algebraic_closure_of_K)
            if hasattr(witness, 'trdeg_K_bar_P') and hasattr(witness, 'trdeg_K_P'):
                neg_q = bool(witness.trdeg_K_bar_P != witness.trdeg_K_P)
            else:
                neg_q = bool(getattr(witness, 'neg_Q', False))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try as an object with P, K, K_bar attributes
    try:
        P = getattr(witness, 'P', None)
        K = getattr(witness, 'K', None)
        K_bar = getattr(witness, 'K_bar', None)
        
        if P is not None and K is not None and K_bar is not None:
            if callable(getattr(K, 'prime_subfield', None)):
                h1 = (P == K.prime_subfield())
            elif hasattr(K, 'prime_subfield'):
                h1 = (P == K.prime_subfield)
            elif callable(getattr(P, 'is_prime_subfield_of', None)):
                h1 = P.is_prime_subfield_of(K)
                
            if callable(getattr(K_bar, 'is_algebraic_closure_of', None)):
                h2 = K_bar.is_algebraic_closure_of(K)
            elif hasattr(K, 'algebraic_closure'):
                h2 = (K_bar == K.algebraic_closure)
                
            if callable(getattr(K_bar, 'trdeg', None)) and callable(getattr(K, 'trdeg', None)):
                neg_q = (K_bar.trdeg(P) != K.trdeg(P))
            elif hasattr(K_bar, 'trdeg') and hasattr(K, 'trdeg'):
                neg_q = (K_bar.trdeg != K.trdeg)
                
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 4. Try as a tuple (P, K, K_bar)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            P, K, K_bar = witness
            
            if callable(getattr(K, 'prime_subfield', None)):
                h1 = (P == K.prime_subfield())
            elif hasattr(K, 'prime_subfield'):
                h1 = (P == K.prime_subfield)
            elif hasattr(K, 'char'):
                if K.char == 0:
                    h1 = (P == QQ)
                else:
                    h1 = (P == GF(K.char))
                    
            if callable(getattr(K_bar, 'is_algebraic_closure_of', None)):
                h2 = K_bar.is_algebraic_closure_of(K)
            elif hasattr(K, 'algebraic_closure'):
                h2 = (K_bar == K.algebraic_closure)
            else:
                h2 = getattr(K_bar, 'is_alg_closure', False) and getattr(K_bar, 'base_field', None) == K
                
            if callable(getattr(K_bar, 'trdeg', None)) and callable(getattr(K, 'trdeg', None)):
                neg_q = (K_bar.trdeg(P) != K.trdeg(P))
            elif hasattr(K_bar, 'trdeg') and hasattr(K, 'trdeg'):
                neg_q = (K_bar.trdeg != K.trdeg)
            else:
                def get_trdeg(domain):
                    if isinstance(domain, FractionField):
                        return len(domain.gens) + get_trdeg(domain.domain)
                    elif isinstance(domain, AlgebraicField):
                        return get_trdeg(domain.domain)
                    elif hasattr(domain, 'gens') and hasattr(domain, 'domain'):
                        return len(domain.gens) + get_trdeg(domain.domain)
                    return 0
                neg_q = (get_trdeg(K_bar) != get_trdeg(K))
                
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 5. Try as an object with specific methods
    try:
        if callable(getattr(witness, 'is_P_prime_subfield_of_K', None)):
            h1 = witness.is_P_prime_subfield_of_K()
        if callable(getattr(witness, 'is_K_bar_algebraic_closure_of_K', None)):
            h2 = witness.is_K_bar_algebraic_closure_of_K()
        if callable(getattr(witness, 'trdeg_K_bar_P', None)) and callable(getattr(witness, 'trdeg_K_P', None)):
            neg_q = (witness.trdeg_K_bar_P() != witness.trdeg_K_P())
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: P is the prime subfield of K",
    "H_2: K_bar is the algebraic closure of K",
    "¬Q: The transcendence degree of K_bar over P is not equal to the transcendence degree of K over P"
]

N_HYP = 2
NEG_Q_INDEX = 2