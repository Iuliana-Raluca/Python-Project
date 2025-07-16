class Validator:
    @staticmethod
    def validate_positive_int(value):
        if not isinstance(value, int):
            raise ValueError("Valoarea introdusa trebuie sa fie un nr intreg")
        if value < 0:
            raise ValueError("Valoarea trebuie sa fie pozitiva.")
