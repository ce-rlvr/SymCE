import sympy
from sympy import S, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.polys.domains import CC as PolyCC

# Top-level setup: named object bindings
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

CC = S.Complexes
QQ = S.Rationals
RR = S.Reals

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Extract F
        F = None
        if isinstance(witness, dict):
            F = witness.get('F', None)
        elif hasattr(witness, 'F'):
            F = witness.F
        elif isinstance(witness, tuple) and len(witness) >= 1:
            F = witness[0]
            
        # Evaluate H1: F is an algebraically closed field
        if F is not None:
            if F == S.Complexes or F == PolyCC or str(F) in ['CC', 'C', 'Complexes']:
                h1 = True
            elif getattr(F, 'is_algebraically_closed', False):
                h1 = True
            elif isinstance(F, str) and ('algebraically closed' in F.lower() or F == 'CC'):
                h1 = True
        elif isinstance(witness, str) and 'CC' in witness:
            h1 = True

        # Extract I_V_I and rad_I
        I_V_I = None
        rad_I = None
        
        if isinstance(witness, dict) and ('I_V_I' in witness or 'rad_I' in witness):
            I_V_I = witness.get('I_V_I', None)
            rad_I = witness.get('rad_I', None)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            I_V_I = witness[1]
            rad_I = witness[2]
        else:
            # Try to extract from the witness directly
            if hasattr(witness, 'I_V_I'):
                I_V_I = witness.I_V_I
                if callable(I_V_I): I_V_I = I_V_I()
            if hasattr(witness, 'rad_I'):
                rad_I = witness.rad_I
                if callable(rad_I): rad_I = rad_I()
            elif hasattr(witness, 'rad'):
                rad_I = witness.rad
                if callable(rad_I): rad_I = rad_I()
            elif hasattr(witness, 'radical'):
                rad_I = witness.radical
                if callable(rad_I): rad_I = rad_I()
                
        # If not found, try to extract from an inner 'I' object
        if I_V_I is None and rad_I is None:
            I_obj = None
            if isinstance(witness, dict):
                I_obj = witness.get('I', None)
            elif hasattr(witness, 'I'):
                I_obj = witness.I
            elif isinstance(witness, tuple) and len(witness) == 2:
                I_obj = witness[1]
                
            if I_obj is not None:
                if hasattr(I_obj, 'I_V_I'):
                    I_V_I = I_obj.I_V_I
                    if callable(I_V_I): I_V_I = I_V_I()
                if hasattr(I_obj, 'rad_I'):
                    rad_I = I_obj.rad_I
                    if callable(rad_I): rad_I = rad_I()
                elif hasattr(I_obj, 'rad'):
                    rad_I = I_obj.rad
                    if callable(rad_I): rad_I = rad_I()
                elif hasattr(I_obj, 'radical'):
                    rad_I = I_obj.radical
                    if callable(rad_I): rad_I = rad_I()

        # Evaluate neg_Q: I(V(I)) != rad(I)
        if I_V_I is not None and rad_I is not None:
            neg_q = (I_V_I != rad_I)
        else:
            # Fallback to explicit neg_Q flag if provided
            if isinstance(witness, dict) and 'neg_Q' in witness:
                neg_q = bool(witness['neg_Q'])
            elif hasattr(witness, 'neg_Q'):
                neg_q = bool(witness.neg_Q)
                
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "¬Q: I(V(I)) is not equal to the radical of I"
]

N_HYP = 1
NEG_Q_INDEX = 1