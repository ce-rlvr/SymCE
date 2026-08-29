import sympy
from sympy import symbols, Rational, Integer

# Top-level setup: Provide standard counterexamples that the witness expression may reference.
class RingExtension:
    def __init__(self, R, L, is_comm_noeth_domain, is_integrally_closed, integral_closure_is_fg):
        self.R = R
        self.L = L
        self.is_comm_noeth_domain = is_comm_noeth_domain
        self.is_integrally_closed = is_integrally_closed
        self.integral_closure_is_fg = integral_closure_is_fg

# Standard counterexample for dropping "finite" (infinite algebraic extension)
Z_Qbar = RingExtension("Z", "Q_bar", True, True, False)

# Standard counterexample for dropping "separable" (finite inseparable extension)
Fp_xy_insep = RingExtension("k[x,y]", "k(x,y)(x^{1/p}, y^{1/p})", True, True, False)

# A case where the conclusion holds (not a counterexample)
Z_Q = RingExtension("Z", "Q", True, True, True)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        is_Z = False
        is_kxy = False
        l_str = ""
        
        # Parse the witness depending on its type
        if isinstance(witness, RingExtension):
            r_str = str(witness.R).lower().replace(" ", "")
            l_str = str(witness.L).lower().replace(" ", "")
            if r_str in ["z", "zz", "integers", "\\mathbb{z}"]:
                is_Z = True
            elif any(x in r_str for x in ["k[x,y]", "f_p[x,y]", "k[[x,y]]", "f[x,y]", "k[x]", "f_p[x]", "k[[x]]"]):
                is_kxy = True
                
        elif isinstance(witness, dict):
            r_str = str(witness.get("R", "")).lower().replace(" ", "")
            l_str = str(witness.get("L", "")).lower().replace(" ", "")
            if r_str in ["z", "zz", "integers", "\\mathbb{z}"]:
                is_Z = True
            elif any(x in r_str for x in ["k[x,y]", "f_p[x,y]", "k[[x,y]]", "f[x,y]", "k[x]", "f_p[x]", "k[[x]]"]):
                is_kxy = True
                
        elif isinstance(witness, tuple) and len(witness) == 2:
            r_str = str(witness[0]).lower().replace(" ", "")
            l_str = str(witness[1]).lower().replace(" ", "")
            if r_str in ["z", "zz", "integers", "\\mathbb{z}"]:
                is_Z = True
            elif any(x in r_str for x in ["k[x,y]", "f_p[x,y]", "k[[x,y]]", "f[x,y]", "k[x]", "f_p[x]", "k[[x]]"]):
                is_kxy = True
                
        elif isinstance(witness, str):
            s = witness.lower()
            if "r=" in s.replace(" ", "") and "l=" in s.replace(" ", ""):
                s_clean = s.replace(" ", "")
                r_part = s_clean.split("r=")[1].split(",")[0]
                l_part = s_clean.split("l=")[1].split(",")[0]
                if r_part in ["z", "zz", "integers", "\\mathbb{z}"]:
                    is_Z = True
                elif any(x in r_part for x in ["k[x,y]", "f_p[x,y]", "k[[x,y]]", "f[x,y]", "k[x]", "f_p[x]", "k[[x]]"]):
                    is_kxy = True
                l_str = l_part
            else:
                # Tokenize string to find keywords
                s_clean = "".join(c if c.isalnum() else " " for c in s)
                tokens = s_clean.split()
                if any(t in ["z", "zz", "integers"] for t in tokens):
                    is_Z = True
                if any(x in s for x in ["k[x,y]", "f_p[x,y]", "k[[x,y]]", "f[x,y]", "k[x]", "f_p[x]", "k[[x]]"]):
                    is_kxy = True
                l_str = s
                
        # Evaluate hypotheses and negated conclusion based on identified rings
        if is_Z:
            h1 = True
            h2 = True
            if any(x in l_str for x in ["q_bar", "qq_bar", "algebraicclosure", "infinite", "q(sqrt", "q(2^(1/", "q(i,sqrt", "bar"]):
                neg_q = True
                
        if is_kxy:
            h1 = True
            h2 = True
            if any(x in l_str for x in ["inseparable", "1/p", "z^p", "x^(1/p)", "y^(1/p)", "x**(1/p)"]):
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: R is integrally closed in its field of fractions K",
    "¬Q: The integral closure of R in L is NOT a finitely generated R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2