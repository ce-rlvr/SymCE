import sympy
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')
QQ = sympy.QQ
ZZ = sympy.ZZ

def is_valuation_ring(witness):
    """
    Check if the witness is a valuation ring.
    For rings with zero divisors, a standard definition (Manis) implies that 
    any finite commutative ring is its own total ring of fractions and thus 
    trivially a valuation ring of itself.
    """
    # Integer n represents the ring Z/nZ
    if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
        return abs(int(witness)) > 1
        
    # SymPy Fields are valuation rings
    if hasattr(witness, 'is_Field') and witness.is_Field:
        return True
        
    # The integers ZZ is not a valuation ring (its field of fractions is QQ, and e.g. 1/2 not in ZZ)
    if witness == sympy.ZZ:
        return False
        
    # SymPy QuotientRing over ZZ
    if hasattr(witness, 'base_ring') and hasattr(witness, 'base_ideal'):
        if witness.base_ring == sympy.ZZ:
            try:
                gens = witness.base_ideal.gens
                if len(gens) == 1:
                    n = abs(int(gens[0]))
                    return n > 1
            except Exception:
                pass
                
    # Custom finite ring objects
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        try:
            elements = list(witness.elements)
            if len(elements) > 1000:
                return False
            # Must be commutative
            for a in elements:
                for b in elements:
                    if witness.mul(a, b) != witness.mul(b, a):
                        return False
            return True
        except Exception:
            return False
            
    return False

def is_local_ring(witness):
    """
    Check if the witness is a local ring.
    A finite commutative ring is local iff it has a unique maximal ideal,
    which is equivalent to the set of non-units forming an ideal.
    """
    # Integer n represents the ring Z/nZ, which is local iff n is a prime power
    if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
        n = abs(int(witness))
        if n <= 1:
            return False
        factors = factorint(n)
        return len(factors) == 1
        
    # Fields are local rings
    if hasattr(witness, 'is_Field') and witness.is_Field:
        return True
        
    if witness == sympy.ZZ:
        return False
        
    # SymPy QuotientRing over ZZ
    if hasattr(witness, 'base_ring') and hasattr(witness, 'base_ideal'):
        if witness.base_ring == sympy.ZZ:
            try:
                gens = witness.base_ideal.gens
                if len(gens) == 1:
                    n = abs(int(gens[0]))
                    if n <= 1:
                        return False
                    factors = factorint(n)
                    return len(factors) == 1
            except Exception:
                pass
                
    # Custom finite ring objects
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        try:
            elements = list(witness.elements)
            if len(elements) > 1000:
                return False
            one = witness.one
            
            # Find all units
            units = []
            for a in elements:
                for b in elements:
                    if witness.mul(a, b) == one:
                        units.append(a)
                        break
                        
            non_units = [elem for elem in elements if elem not in units]
            
            if not non_units:
                return True  # It's a field
                
            # Check if non-units are closed under addition
            for a in non_units:
                for b in non_units:
                    s = witness.add(a, b)
                    if s not in non_units:
                        return False
                        
            # Check if non-units are closed under multiplication by any ring element
            for a in non_units:
                for r in elements:
                    p = witness.mul(a, r)
                    if p not in non_units:
                        return False
                        
            return True
        except Exception:
            return False
            
    return False

def conditions(witness):
    try:
        h1 = bool(is_valuation_ring(witness))
    except Exception:
        h1 = False
        
    try:
        q = bool(is_local_ring(witness))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a valuation ring",
    "¬Q: R is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1