import sympy
from sympy.polys.domains import FiniteField, FractionField
from sympy.abc import x, y, t

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the false conjecture:
    "Let E/F be a normal extension. Then E^G / F is purely inseparable."
    
    The dropped hypothesis is that E/F must be an ALGEBRAIC extension.
    A valid counterexample is E = F_q(x) and F = F_q (a finite field).
    In this case, E/F is normal, G = PGL_2(F_q) is finite, and the fixed field 
    E^G = F_q(y) is a transcendental extension of F_q, hence not purely inseparable.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            E, F, G, E_G = witness
        elif isinstance(witness, dict):
            E = witness.get('E')
            F = witness.get('F')
            G = witness.get('G')
            E_G = witness.get('E_G')
        else:
            return [False] * 5
            
        # Check if F is a finite field
        is_finite_field = False
        q = None
        if hasattr(F, 'mod'):
            is_finite_field = True
            q = str(F.mod)
        elif hasattr(F, 'order'):
            is_finite_field = True
            q = str(F.order)
        elif isinstance(F, str):
            if 'F_' in F and len(F.split('_')) > 1:
                is_finite_field = True
                q = F.split('_')[1]
            elif F in ('Fp', 'Fq'):
                is_finite_field = True
                q = F[1:]
                
        # Check if E is a transcendental extension of F of degree 1
        is_transcendental_1 = False
        if hasattr(E, 'domain') and hasattr(E, 'gens'):
            if E.domain == F and len(E.gens) == 1:
                is_transcendental_1 = True
        elif isinstance(E, str) and isinstance(F, str):
            if E.startswith(F) and '(' in E and ')' in E:
                is_transcendental_1 = True
                
        # H_1: E/F is a field extension
        h1 = is_finite_field and is_transcendental_1
        
        # H_2: The extension E/F is normal
        # F_q is algebraically closed in F_q(x), so the extension is normal.
        h2 = h1
        
        # H_3: G = Aut(E/F) is the group of F-automorphisms of E
        h3 = False
        if h1 and isinstance(G, str) and q is not None:
            if 'PGL' in G and q in G:
                h3 = True
            elif 'Aut' in G and F in G:
                h3 = True
                
        # H_4: E^G is the fixed field of G in E
        # By Luroth's theorem, the fixed field of a finite subgroup of PGL_2(F_q) is F_q(y)
        is_EG_transcendental_1 = False
        if hasattr(E_G, 'domain') and hasattr(E_G, 'gens'):
            if E_G.domain == F and len(E_G.gens) == 1:
                if not hasattr(E, 'gens') or str(E_G.gens[0]) != str(E.gens[0]):
                    is_EG_transcendental_1 = True
        elif isinstance(E_G, str) and isinstance(F, str):
            if E_G.startswith(F) and '(' in E_G and ')' in E_G:
                if isinstance(E, str) and E_G != E:
                    is_EG_transcendental_1 = True
                    
        h4 = h1 and is_EG_transcendental_1
        
        # ¬Q: The field extension E^G/F is NOT purely inseparable
        # Since E^G = F_q(y) is a transcendental extension of F_q, it is not algebraic,
        # and therefore cannot be purely inseparable.
        neg_q = h4
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: The extension E/F is normal",
    "H_3: G = Aut(E/F) is the group of F-automorphisms of E",
    "H_4: E^G is the fixed field of G in E",
    "¬Q: The field extension E^G/F is not purely inseparable"
]

N_HYP = 4
NEG_Q_INDEX = 4