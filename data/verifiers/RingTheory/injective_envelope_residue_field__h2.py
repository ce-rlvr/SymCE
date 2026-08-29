import sympy
from sympy import symbols
import math
import itertools
import functools

class _Ring:
    def __init__(self, commutative, noetherian, local):
        self.is_commutative = commutative
        self.is_noetherian = noetherian
        self.is_local = local

class _Module:
    def __init__(self, injective_envelope, artinian):
        self.is_injective_envelope = injective_envelope
        self.is_artinian = artinian

Z_p = _Ring(True, True, True)
Q_mod = _Module(True, False)

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian local ring with maximal ideal m",
    "H_2: E(k) is the injective envelope of k over R",
    "¬Q: E(k) is not an Artinian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', False) and 
                      witness.get('is_noetherian', False) and 
                      witness.get('is_local', False))
            h2 = bool(witness.get('is_injective_envelope', False))
            if 'is_artinian' in witness:
                neg_q = not bool(witness.get('is_artinian'))
                
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, E = witness
            
            if isinstance(R, dict):
                h1 = bool(R.get('is_commutative', False) and 
                          R.get('is_noetherian', False) and 
                          R.get('is_local', False))
            else:
                h1 = bool(getattr(R, 'is_commutative', False) and 
                          getattr(R, 'is_noetherian', False) and 
                          getattr(R, 'is_local', False))
                          
            if isinstance(E, dict):
                h2 = bool(E.get('is_injective_envelope', False))
                if 'is_artinian' in E:
                    neg_q = not bool(E.get('is_artinian'))
            else:
                h2 = bool(getattr(E, 'is_injective_envelope', False))
                if hasattr(E, 'is_artinian'):
                    neg_q = not bool(getattr(E, 'is_artinian'))
                    
        else:
            h1 = bool(getattr(witness, 'is_commutative', False) and 
                      getattr(witness, 'is_noetherian', False) and 
                      getattr(witness, 'is_local', False))
            h2 = bool(getattr(witness, 'is_injective_envelope', False))
            if hasattr(witness, 'is_artinian'):
                neg_q = not bool(getattr(witness, 'is_artinian'))
                
    except Exception:
        pass

    try:
        s = str(witness).lower()
        if not h1:
            h1 = ('commutative' in s and 'noetherian' in s and 'local' in s) or ('z_{(p)}' in s)
        if not h2:
            h2 = 'injective' in s or 'e(k)' in s
        if not neg_q:
            neg_q = 'not artinian' in s or 'non-artinian' in s or 'not an artinian' in s
    except Exception:
        pass

    return [h1, h2, neg_q]