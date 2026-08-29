import sympy
import sympy.combinatorics
import sympy.matrices

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
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_bool_attr(obj, names):
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if callable(val):
                try:
                    val = val()
                except Exception:
                    pass
            return bool(val)
        elif isinstance(obj, dict) and name in obj:
            val = obj[name]
            if callable(val):
                try:
                    val = val()
                except Exception:
                    pass
            return bool(val)
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, type):
            try:
                witness = witness()
            except Exception:
                pass

        is_PIR = None
        all_max_principal = None
        
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], bool) and isinstance(witness[1], bool):
                is_PIR, all_max_principal = witness

        if is_PIR is None:
            is_PIR = get_bool_attr(witness, ["is_PIR", "is_principal_ideal_ring", "principal_ideal_ring"])
        if all_max_principal is None:
            all_max_principal = get_bool_attr(witness, ["all_max_ideals_principal", "every_maximal_ideal_is_principal", "maximal_ideals_principal", "max_ideals_principal"])
            
        if is_PIR is None or all_max_principal is None:
            if isinstance(witness, str):
                s = witness.lower()
                if "valuation" in s or "local" in s:
                    if "pid" in s or ("pir" in s and "not" not in s):
                        is_PIR = True
                        all_max_principal = True
                    else:
                        is_PIR = False
                        all_max_principal = True
                elif "z[x]" in s or "q[x,y]" in s:
                    is_PIR = False
                    all_max_principal = False
                else:
                    is_PIR = False
                    all_max_principal = False
            else:
                if witness == sympy.ZZ or witness == sympy.QQ:
                    is_PIR = True
                    all_max_principal = True
                elif hasattr(sympy.polys.rings, 'PolyRing') and isinstance(witness, sympy.polys.rings.PolyRing):
                    if witness.domain.is_Field and len(witness.gens) == 1:
                        is_PIR = True
                        all_max_principal = True
                    else:
                        is_PIR = False
                        all_max_principal = False
                else:
                    return [False]
                    
        neg_Q = (bool(is_PIR) != bool(all_max_principal))
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: R is a principal ideal ring iff every maximal ideal of R is a principal ideal (fails)"
]
N_HYP = 0
NEG_Q_INDEX = 0