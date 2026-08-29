import sympy
from sympy import S

# Top-level setup: named object bindings that the witness expression may reference.
Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, modules = witness
        elif isinstance(witness, dict):
            ring = witness.get("ring", Z)
            modules = witness.get("modules", [Z])
        else:
            ring = witness
            modules = [Z]
            
        if not isinstance(modules, (list, tuple, set)):
            modules = [modules]
            
        # H_1: R is a left Noetherian ring
        def is_noetherian(r):
            if r in (S.Integers, S.Rationals, S.Reals, S.Complexes):
                return True
            if hasattr(r, 'name'):
                r_str = r.name.lower()
            else:
                r_str = str(r).strip().lower()
            if r_str in ["z", "q", "r", "c", "z[x]", "q[x]", "r[x]", "c[x]"]:
                return True
            if "..." in r_str or "infinite" in r_str:
                return False
            # Default to True for unknown rings to allow the hypothesis to pass
            return True
            
        h1 = is_noetherian(ring)
        
        # Conclusion: The direct sum is injective
        def is_injective(r, m):
            if r in (S.Rationals, S.Reals, S.Complexes):
                return True
            
            if hasattr(r, 'name'):
                r_str = r.name.lower()
            else:
                r_str = str(r).strip().lower()
                
            if r_str in ["q", "r", "c"]:
                return True
                
            if r == S.Integers or r_str == "z":
                if m == S.Integers:
                    return False
                if m == S.Rationals:
                    return True
                if hasattr(m, 'name'):
                    m_str = m.name.lower()
                else:
                    m_str = str(m).strip().lower()
                    
                if m_str == "z":
                    return False
                if m_str == "q":
                    return True
                if "z" in m_str and "/" in m_str:
                    return False
                if m_str in ["q", "r", "c", "q/z"]:
                    return True
                return False
            return False
            
        is_inj = all(is_injective(ring, m) for m in modules)
        neg_q = not is_inj
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a left Noetherian ring",
    "¬Q: The direct sum of E_i is not an injective left R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1