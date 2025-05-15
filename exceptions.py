# ----- Top-Level Errors ----- #

class ScrollError(Exception):
    def __init__(self, message):
        super().__init__(message)

# ----- Rune Errors ----- #

class RuneError(ScrollError):
    def __init__(self, message):
        super().__init__(message)

class RuneAlreadyWrittenError(RuneError):
    def __init__(self, name):
        super().__init__(f"The rune '{name}' is already written.")

class RuneNotWrittenError(RuneError):
    def __init__(self, name):
        super().__init__(f"The rune '{name}' has not yet been written.")

class DormantRuneError(RuneError):
    def __init__(self, name):
        super().__init__(f"The rune '{name}' is dormant, and cannot yet be used.")

class NoPastError(RuneError):
    def __init__(self, name):
        super().__init__(f"The rune '{name}' has no past.")

class SealedRuneError(RuneError):
    def __init__(self, name):
        super().__init__(f"The rune '{name}' is sealed.")

class TransmutationError(RuneError):
    def __init__(self, vfrom, vto):
        super().__init__(f"Failed to transmute from '{vfrom}' to '{vto}'.")

class FundamentalRuneError(RuneError):
    def __init__(self, name):
        super().__init__(f"'{name}' is fundamental to the arcane, and may not be confined to a rune.")


# ----- Spell Errors ----- #

class SpellError(ScrollError):
    def __init__(self, message):
        super().__init__(message)

class UnknownSpellError(SpellError):
    def __init__(self, name):
        super().__init__(f"Unknown spell:'{name}'")

class CarelessSpellError(SpellError):
    def __init__(self, message):
        super().__init__(message)

class MeasureError(SpellError):
    def __init__(self, message):
        super().__init__(message)

