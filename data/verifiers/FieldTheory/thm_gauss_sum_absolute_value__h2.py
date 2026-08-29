import sympy
import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (q, chi, psi) where:
      - q is a prime number (representing the finite field F_q).
      - chi is a list of length q representing the values of a multiplicative character.
      - psi is a list of length q representing the values of an additive character.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        q, chi_in, psi_in = witness
        
        # We restrict to prime fields for simplicity of verification.
        # A counterexample for a prime field is sufficient to disprove the general conjecture.
        if not sympy.isprime(q):
            return [False, False, False]
            
        if len(chi_in) != q or len(psi_in) != q:
            return [False, False, False]
            
        chi = [complex(c) for c in chi_in]
        psi = [complex(p) for p in psi_in]
        
        # H_1: F_q is a finite field and chi is a multiplicative character
        h1 = True
        if abs(chi[0]) > 1e-7:
            h1 = False
        if abs(chi[1] - 1) > 1e-7:
            h1 = False
        for x in range(q):
            for y in range(q):
                if abs(chi[(x * y) % q] - chi[x] * chi[y]) > 1e-7:
                    h1 = False
                    break
            if not h1:
                break
                
        # H_2: psi is a non-trivial additive character
        h2 = True
        if abs(psi[0] - 1) > 1e-7:
            h2 = False
        for x in range(q):
            for y in range(q):
                if abs(psi[(x + y) % q] - psi[x] * psi[y]) > 1e-7:
                    h2 = False
                    break
            if not h2:
                break
        
        is_trivial = True
        for x in range(q):
            if abs(psi[x] - 1) > 1e-7:
                is_trivial = False
                break
        if is_trivial:
            h2 = False
            
        # ¬Q: The absolute value of the Gauss sum G(chi, psi) is NOT equal to sqrt(q)
        neg_q = False
        G = sum(chi[x] * psi[x] for x in range(q))
        if abs(abs(G) - math.sqrt(q)) > 1e-7:
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements (and chi is a multiplicative character)",
    "H_2: psi is a non-trivial additive character of F_q",
    "¬Q: The absolute value of the Gauss sum G(chi, psi) is not equal to sqrt(q)"
]

N_HYP = 2
NEG_Q_INDEX = 2