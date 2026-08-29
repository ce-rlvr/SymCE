import sympy
from sympy import Symbol, QQ, ZZ
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not have built-in representations for arbitrary algebraic closures 
# and field homomorphisms, we provide mock classes to allow the construction of a formal witness.

class Field:
    def __init__(self, name="F"):
        self.name = str(name)
        
    def __eq__(self, other):
        return isinstance(other, Field) and self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
        
    def __repr__(self):
        return f"Field({self.name})"

class AlgebraicClosure(Field):
    def __init__(self, base_field):
        name = getattr(base_field, 'name', str(base_field))
        super().__init__(name=f"{name}_alg")
        self.base_field = base_field
        
    def __eq__(self, other):
        return isinstance(other, AlgebraicClosure) and self.base_field == other.base_field
        
    def __hash__(self):
        return hash(("AlgClosure", self.base_field))
        
    def __repr__(self):
        return f"AlgebraicClosure({self.base_field})"

class FieldHomomorphism:
    def __init__(self, domain, codomain, is_injective=True, is_surjective=True):
        self.domain = domain
        self.codomain = codomain
        # A valid field homomorphism must be injective (fields have no non-trivial ideals)
        self.is_injective = is_injective
        self.is_surjective = is_surjective

    def is_automorphism(self):
        return self.domain == self.codomain and self.is_injective and self.is_surjective
        
    def __repr__(self):
        return f"FieldHomomorphism({self.domain} -> {self.codomain}, inj={self.is_injective}, surj={self.is_surjective})"

def is_valid_field(obj):
    if isinstance(obj, Field):
        return True
    if isinstance(obj, Symbol):
        return True
    if hasattr(obj, 'is_Field') and obj.is_Field:
        return True
    if type(obj).__name__ in ['FractionField', 'RationalField', 'RealField', 'ComplexField', 'AlgebraicField']:
        return True
    return False

def is_alg_closure(obj, F):
    if isinstance(obj, AlgebraicClosure) and obj.base_field == F:
        return True
    if type(obj).__name__ == 'AlgebraicClosure' and getattr(obj, 'base_field', None) == F:
        return True
    return False

def is_field_hom(obj, K):
    if isinstance(obj, FieldHomomorphism) and obj.domain == K and obj.codomain == K and obj.is_injective:
        return True
    if type(obj).__name__ == 'FieldHomomorphism' and getattr(obj, 'domain', None) == K and getattr(obj, 'codomain', None) == K and getattr(obj, 'is_injective', False):
        return True
    return False

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    try:
        # Unpack the witness. It can be a dictionary, a tuple (F, K, sigma), or just sigma.
        if isinstance(witness, dict):
            F = witness.get("F")
            K = witness.get("K")
            sigma = witness.get("sigma")
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, K, sigma = witness
        else:
            sigma = witness
            K = getattr(sigma, 'domain', None)
            F = getattr(K, 'base_field', None)

        # H_1: F is a field
        if is_valid_field(F):
            h1 = True
            
        # H_2: K is an algebraic closure of F
        if is_alg_closure(K, F):
            h2 = True
            
        # H_3: sigma: K -> K is a field homomorphism
        if is_field_hom(sigma, K):
            h3 = True
            
        # ¬Q: sigma is not a field automorphism of K
        if h3:
            if hasattr(sigma, 'is_automorphism'):
                neg_q = not sigma.is_automorphism()
            else:
                neg_q = not (getattr(sigma, 'is_injective', True) and getattr(sigma, 'is_surjective', True))
            
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is an algebraic closure of F",
    "H_3: sigma: K -> K is a field homomorphism",
    "¬Q: sigma is not a field automorphism of K"
]

N_HYP = 3
NEG_Q_INDEX = 3