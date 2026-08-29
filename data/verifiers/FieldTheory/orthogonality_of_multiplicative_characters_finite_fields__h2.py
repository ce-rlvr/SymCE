import sympy
from sympy import expand
from sympy.ntheory import factorint, divisors

# Top-level setup
# (No specific named objects are required for this domain)

def is_valid_character_multiset(q, chi_values):
    if len(chi_values) != q - 1:
        return False
    
    S = []
    for k in range(1, q):
        try:
            sk = sum(v**k for v in chi_values)
            S.append(sk)
        except Exception:
            return False
        
    for d in divisors(q - 1):
        valid = True
        for k in range(1, q):
            expected = (q - 1) if k % d == 0 else 0
            diff = S[k-1] - expected
            if diff == 0:
                continue
            
            try:
                diff_simp = expand(diff)
                if diff_simp == 0:
                    continue
                if hasattr(diff_simp, 'evalf'):
                    diff_val = complex(diff_simp.evalf())
                else:
                    diff_val = complex(diff_simp)
                if abs(diff_val) < 1e-7:
                    continue
            except Exception:
                pass
            
            valid = False
            break
            
        if valid:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        q, chi_values_iter = witness
        chi_values = list(chi_values_iter)
    except Exception:
        return [False, False]
        
    # H_1: F_q is a finite field with q elements and chi is a multiplicative character
    try:
        h1 = False
        if isinstance(q, int) and q >= 2:
            if len(factorint(q)) == 1:
                if is_valid_character_multiset(q, chi_values):
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: The sum of chi(x) over F_q^x is not equal to 0
    try:
        total = sum(chi_values)
        
        neg_q = True
        if total == 0:
            neg_q = False
        else:
            try:
                total_simp = expand(total)
                if total_simp == 0:
                    neg_q = False
                else:
                    if hasattr(total_simp, 'evalf'):
                        total_val = complex(total_simp.evalf())
                    else:
                        total_val = complex(total_simp)
                    if abs(total_val) < 1e-7:
                        neg_q = False
            except Exception:
                pass
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements and chi is a multiplicative character",
    "¬Q: The sum of chi(x) over F_q^x is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1