import sympy

class Ring:
    def __init__(self, name, is_commutative, is_local):
        self.name = name
        self.is_commutative = is_commutative
        self.is_local = is_local
        
    def __eq__(self, other):
        if not isinstance(other, Ring):
            return False
        return self.name == other.name

class RModule:
    def __init__(self, name, ring, is_fg, is_zero):
        self.name = name
        self.ring = ring
        self.is_fg = is_fg
        self.is_zero = is_zero

# Named bindings for rings
LocalRing_Zp = Ring("Z_p", is_commutative=True, is_local=True)
LocalRing_Q = Ring("Q", is_commutative=True, is_local=True)
NonLocalRing_Z = Ring("Z", is_commutative=True, is_local=False)
NonCommutativeRing = Ring("Weyl", is_commutative=False, is_local=False)

# Named bindings for modules
Module_Zp_nonzero = RModule("Z_p", LocalRing_Zp, is_fg=True, is_zero=False)
Module_Zp_zero = RModule("0", LocalRing_Zp, is_fg=True, is_zero=True)

Module_Q_nonzero = RModule("Q", LocalRing_Q, is_fg=True, is_zero=False)
Module_Q_zero = RModule("0", LocalRing_Q, is_fg=True, is_zero=True)

Module_Z_nonzero = RModule("Z", NonLocalRing_Z, is_fg=True, is_zero=False)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a module object or a tuple (Ring, Module).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, M = witness
            else:
                return [False, False, False, False]
        else:
            M = witness
            R = getattr(M, 'ring', None)
            
        # H_1: R is a commutative ring
        h1 = getattr(R, 'is_commutative', False)
        
        # H_2: R is a local ring with maximal ideal m
        h2 = getattr(R, 'is_local', False)
        
        # H_3: M is a finitely generated R-module
        m_ring = getattr(M, 'ring', None)
        h3 = getattr(M, 'is_fg', False) and (m_ring is R or m_ring == R)
        
        # ¬Q: M is not the zero module
        neg_q = not getattr(M, 'is_zero', True)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: M is a finitely generated R-module",
    "¬Q: M is not the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3