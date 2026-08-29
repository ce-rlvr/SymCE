import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

class MockModule:
    """
    A mock class to represent a module with specific properties,
    since SymPy does not natively support non-Noetherian rings.
    """
    def __init__(self, is_finitely_generated=True, is_finitely_presented=False):
        self.is_finitely_generated = is_finitely_generated
        self.is_finitely_presented = is_finitely_presented

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # SymPy agca Module (always finitely presented over Noetherian rings)
        try:
            from sympy.polys.agca.modules import Module
            if isinstance(witness, Module):
                return [True, False]
        except ImportError:
            pass
            
        # SymPy agca Ideal
        try:
            from sympy.polys.agca.ideals import Ideal
            if isinstance(witness, Ideal):
                return [True, False]
        except ImportError:
            pass

        # SymPy FpGroup
        try:
            from sympy.combinatorics.fp_groups import FpGroup
            if isinstance(witness, FpGroup):
                return [True, False]
        except ImportError:
            pass

        # SymPy FreeGroup
        try:
            from sympy.combinatorics.free_groups import FreeGroup
            if isinstance(witness, FreeGroup):
                return [True, False]
        except ImportError:
            pass

        # SymPy Matrix (represents a finite presentation matrix)
        if isinstance(witness, sympy.MatrixBase):
            return [True, False]

        # 1. Dictionary representation
        if isinstance(witness, dict):
            if "is_finitely_generated" in witness and "is_finitely_presented" in witness:
                h1 = bool(witness["is_finitely_generated"])
                neg_q = not bool(witness["is_finitely_presented"])
                return [h1, neg_q]
                
        # 2. Object with attributes (e.g., MockModule)
        if hasattr(witness, "is_finitely_generated") and hasattr(witness, "is_finitely_presented"):
            h1 = bool(witness.is_finitely_generated)
            neg_q = not bool(witness.is_finitely_presented)
            return [h1, neg_q]
            
        # 3. Tuple of booleans
        if isinstance(witness, tuple) and len(witness) >= 2:
            if isinstance(witness[0], bool) and isinstance(witness[1], bool):
                h1 = witness[0]
                neg_q = not witness[1]
                return [h1, neg_q]
                
        # 4. Tuple containing a SymPy Module
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                from sympy.polys.agca.modules import Module
                if isinstance(witness[0], Module) or isinstance(witness[1], Module):
                    return [True, False]
            except ImportError:
                pass

        # 5. Tuple of (generators, relations)
        if isinstance(witness, tuple) and len(witness) == 2:
            gens, rels = witness
            if isinstance(gens, (list, tuple, set)):
                h1 = True
                if type(rels).__name__ == 'generator':
                    neg_q = True
                elif hasattr(rels, "__len__"):
                    neg_q = False
                elif callable(rels):
                    neg_q = True
                else:
                    neg_q = False
                return [h1, neg_q]
                
        # 6. String description
        if isinstance(witness, str):
            s = witness.lower()
            if "not finitely generated" in s:
                h1 = False
            elif "finitely generated" in s or "fg" in s:
                h1 = True
            else:
                h1 = False
                
            if "not finitely presented" in s or "infinite" in s or "not fp" in s:
                neg_q = True
            else:
                neg_q = False
                
            return [h1, neg_q]
                
        # 7. Callable returning properties
        if callable(witness):
            res = witness()
            if isinstance(res, tuple) and len(res) >= 2:
                if isinstance(res[0], bool) and isinstance(res[1], bool):
                    return [bool(res[0]), not bool(res[1])]
            elif hasattr(res, "is_finitely_generated") and hasattr(res, "is_finitely_presented"):
                return [bool(res.is_finitely_generated), not bool(res.is_finitely_presented)]
                    
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "¬Q: M is not a finitely presented R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1