import sympy
from sympy.polys.domains import Domain
import math
import itertools
import functools

# Top-level setup for potential witness expressions
QQ = sympy.QQ
ZZ = sympy.ZZ
x = sympy.Symbol('x')
y = sympy.Symbol('y')
p = sympy.Symbol('p')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If K is a perfect field, then any extension L over K has a separating transcendence basis."
    (The dropped hypothesis is that L is finitely generated over K).
    """
    h1 = False
    neg_q = False
    
    try:
        # Handle dictionary-based witness
        if isinstance(witness, dict):
            if "K_is_perfect" in witness:
                h1 = bool(witness["K_is_perfect"])
            if "has_separating_transcendence_basis" in witness:
                neg_q = not bool(witness["has_separating_transcendence_basis"])
                
        # Handle object-based witness with attributes
        elif hasattr(witness, "K_is_perfect"):
            h1 = bool(witness.K_is_perfect)
            neg_q = not bool(getattr(witness, "has_separating_transcendence_basis", True))
            
        # Handle string, tuple of strings, or SymPy domains
        else:
            if isinstance(witness, tuple) and len(witness) == 2:
                K, L = witness
            else:
                K, L = witness, witness
                
            K_str = str(K).lower()
            L_str = str(L).lower()
            
            # Check if K is perfect
            # Perfect fields include char 0 fields (Q, R, C) and finite fields (F_p, GF(p))
            is_char_0 = any(kw in K_str for kw in ["qq", "rational", "real", "complex", "char 0", "characteristic 0"]) or K_str == "q"
            is_char_p_perfect = any(kw in K_str for kw in ["f_p", "gf", "finite field", "perfect", "f_q", "f_2", "f_3", "f_5", "char p", "characteristic p"])
            
            # Exclude explicitly imperfect fields like F_p(t)
            if any(kw in K_str for kw in ["(t)", "(x)", "not perfect", "imperfect"]) and "perfect" not in K_str:
                is_char_p_perfect = False
                is_char_0 = False
                
            if is_char_0 or is_char_p_perfect:
                h1 = True
                
            # Check if L lacks a separating transcendence basis (neg_Q)
            # In char 0, all extensions have a separating transcendence basis, so neg_Q is False.
            # In char p > 0, a counterexample must be an infinite extension adjoining p-th roots.
            if not is_char_0 and is_char_p_perfect:
                # Perfect/algebraic closures of transcendental extensions lack a separating transcendence basis
                if ("perfect closure" in L_str or "algebraic closure" in L_str) and any(kw in L_str for kw in ["(x)", "(t)", "y", "z", "transcendental", "fraction", "rational"]):
                    neg_q = True
                else:
                    # Look for infinite sequences of p-th roots, e.g., F_p(x, x^{1/p}, x^{1/p^2}, ...)
                    has_inf = any(kw in L_str for kw in ["...", "infinite", "not finitely generated", "for all", "infty", "infinity"])
                    has_proot = any(kw in L_str for kw in ["1/p", "p^", "p**", "root", "1/2", "1/3"])
                    if has_inf and has_proot:
                        neg_q = True
                        
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a perfect field",
    "¬Q: L does not have a separating transcendence basis over K"
]

N_HYP = 1
NEG_Q_INDEX = 1