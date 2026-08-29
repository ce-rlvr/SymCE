import sympy
from sympy import Poly, Symbol, S
from sympy.ntheory import isprime
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "¬Q: The equivalence between L^P being normal and P being normal fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Parse the witness
        if isinstance(witness, dict):
            if 'f' in witness and 'p' in witness:
                f = witness['f']
                p = witness['p']
            elif 'L_is_normal' in witness:
                h1 = witness.get('P_is_Sylow', True)
                LP_is_normal = witness.get('LP_is_normal', False)
                P_is_normal = witness.get('P_is_normal', True)
                conclusion = (LP_is_normal == P_is_normal)
                return [bool(h1), not conclusion]
            else:
                return [False, False]
        elif hasattr(witness, 'f') and hasattr(witness, 'p'):
            f = witness.f
            p = witness.p
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 2:
                f, p = witness
            else:
                return [False, False]
        else:
            f = witness
            p = 2  # Default prime for standard counterexamples like x**3 - 2
            
        if isinstance(f, str):
            f = sympy.sympify(f)
            
        free = list(f.free_symbols)
        if not free:
            return [False, False]
        var = free[0]
        f_poly = Poly(f, var, domain='QQ')
        
        # H1: P is a Sylow p-subgroup of G
        # We construct G = Aut(L/Q) where L = Q[x]/(f). 
        # P is defined as a Sylow p-subgroup of G.
        # This is valid if p is prime and f is irreducible.
        h1 = isprime(p) and f_poly.is_irreducible
        if not h1:
            return [False, False]
            
        # Determine the order of G = Aut(L/Q) and whether L/Q is a normal extension
        deg = f_poly.degree()
        if deg == 1:
            G_order = 1
            L_is_normal = True
        elif deg == 2:
            G_order = 2
            L_is_normal = True
        elif deg == 3:
            disc = S(f_poly.discriminant())
            if disc.is_square:
                G_order = 3
                L_is_normal = True
            else:
                G_order = 1
                L_is_normal = False
        elif deg == 4:
            if f == var**4 - 2:
                G_order = 2
                L_is_normal = False
            else:
                return [False, False]
        else:
            return [False, False]
            
        # P is a Sylow p-subgroup of G
        P_order = 1
        temp = G_order
        while temp % p == 0:
            P_order *= p
            temp //= p
            
        # For G_order <= 3, G is abelian, so all subgroups (including P) are normal
        P_is_normal = True 
        
        # Determine if the fixed field L^P is normal over Q
        if G_order == 1:
            LP_is_normal = L_is_normal
        elif G_order == 2:
            if P_order == 2:
                LP_is_normal = True
            else:
                LP_is_normal = L_is_normal
        elif G_order == 3:
            LP_is_normal = True
            
        # Conclusion: L^P is normal iff P is normal
        conclusion = (LP_is_normal == P_is_normal)
        
        return [bool(h1), not conclusion]
    except Exception:
        return [False, False]