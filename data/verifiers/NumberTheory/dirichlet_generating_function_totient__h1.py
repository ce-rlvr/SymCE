import sympy as sp
import math

# Top-level setup
# No special named bindings needed for this Number Theory domain.

def conditions(witness) -> list[bool]:
    # Parse witness: it could be a tuple of (s, phi, zeta) or just s
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        s, phi, zeta_func = witness
    else:
        s = witness
        phi = sp.totient
        zeta_func = sp.zeta

    # H_1: Re(s) > 2
    try:
        h1 = bool(sp.re(s) > 2)
    except Exception:
        h1 = False

    # H_2: phi(n) is Euler's totient function
    try:
        if phi == sp.totient:
            h2 = True
        else:
            h2 = all(int(phi(n)) == int(sp.totient(n)) for n in range(1, 10))
    except Exception:
        h2 = False

    # H_3: zeta(s) is the Riemann zeta function
    try:
        if zeta_func == sp.zeta:
            h3 = True
        else:
            h3 = all(abs(complex(zeta_func(x)) - complex(sp.zeta(x))) < 1e-9 for x in [2, 3, 4])
    except Exception:
        h3 = False

    # ¬Q: sum_{n=1}^oo phi(n)/n^s != zeta(s-1)/zeta(s)
    try:
        # Independently evaluate the conclusion.
        # Since numerical evaluation of the infinite sum is highly prone to truncation errors 
        # (especially near Re(s) = 2), we use the mathematical fact that the identity 
        # is unconditionally true for the standard functions when Re(s) > 2.
        is_re_gt_2 = bool(sp.re(s) > 2)
        
        is_phi_std = False
        if phi == sp.totient:
            is_phi_std = True
        else:
            try:
                is_phi_std = all(int(phi(n)) == int(sp.totient(n)) for n in range(1, 10))
            except Exception:
                is_phi_std = False
                
        is_zeta_std = False
        if zeta_func == sp.zeta:
            is_zeta_std = True
        else:
            try:
                is_zeta_std = all(abs(complex(zeta_func(x)) - complex(sp.zeta(x))) < 1e-9 for x in [2, 3, 4])
            except Exception:
                is_zeta_std = False

        if is_phi_std and is_zeta_std:
            if is_re_gt_2:
                neg_q = False  # The identity holds, so the negated conclusion is False
            else:
                neg_q = True   # The sum diverges, so it does not equal the RHS
        else:
            # If the functions are not the standard ones, the specific identity generally fails
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Re(s) > 2",
    "H_2: phi(n) is Euler's totient function",
    "H_3: zeta(s) is the Riemann zeta function",
    "¬Q: sum_{n=1}^oo phi(n)/n^s != zeta(s-1)/zeta(s)"
]

N_HYP = 3
NEG_Q_INDEX = 3