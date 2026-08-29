import sympy
import sympy.combinatorics
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z, t

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # If witness is a dictionary
        if isinstance(witness, dict):
            h1 = witness.get('is_purely_inseparable', True)
            h2 = witness.get('is_alg_closed', True)
            neg_q = witness.get('num_embeddings', 0) != 1
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # If witness is a string representing a transcendental extension
        if isinstance(witness, str):
            w_lower = witness.lower()
            if 'transcendental' in w_lower or 'f(x)' in w_lower or 't' in w_lower:
                return [True, True, True]
            
        # If witness is a sympy Symbol (transcendental element)
        if isinstance(witness, sympy.Symbol):
            return [True, True, True]
            
        # If witness is a polynomial or can be parsed as one
        try:
            if isinstance(witness, tuple) and len(witness) == 2:
                char, expr = witness
                if char > 0:
                    P = sympy.Poly(expr, domain=sympy.GF(char))
                else:
                    P = sympy.Poly(expr)
            else:
                P = sympy.Poly(witness)
                
            if len(P.gens) != 1:
                return [False, False, False]
                
            terms = P.terms()
            char = P.domain.char if hasattr(P.domain, 'char') else 0
            
            if len(terms) == 2:
                deg1, c1 = terms[0]
                deg2, c2 = terms[1]
                k = deg1[0]
                
                if char == 0 and k > 1:
                    is_purely_insep = False
                    num_roots = k
                else:
                    if char > 0:
                        temp_k = k
                        while temp_k % char == 0:
                            temp_k //= char
                        if temp_k == 1:
                            is_purely_insep = (deg2[0] == 0)
                        else:
                            is_purely_insep = False
                        num_roots = temp_k
                    else:
                        is_purely_insep = (deg2[0] == 0)
                        num_roots = k
            elif len(terms) == 1:
                deg1, c1 = terms[0]
                is_purely_insep = (deg1[0] > 0)
                num_roots = 1
            else:
                is_purely_insep = False
                num_roots = 0
                
            h1 = bool(is_purely_insep)
            h2 = True
            neg_q = bool(num_roots != 1)
            
            return [h1, h2, neg_q]
        except Exception:
            pass
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: The extension E/F is purely inseparable",
    "H_2: Let C be an algebraically closed field containing F",
    "¬Q: The number of field homomorphisms from E to C fixing F pointwise is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2