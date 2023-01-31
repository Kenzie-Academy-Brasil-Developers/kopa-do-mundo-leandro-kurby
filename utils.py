class NegativeTitlesError(Exception):
    def __init__(self, message: dict):
        self.message = message


class InvalidYearCupError(Exception):
    def __init__(self, message: dict):
        self.message = message


class ImpossibleTitlesError(Exception):
    def __init__(self, message: dict):
        self.message = message


def data_processing(data: dict):
    year = int(data["first_cup"][0: 4])

    if data["titles"] < 0:
        raise NegativeTitlesError({"error": "titles cannot be negative"})

    if year < 1930 or (year - 1930) % 4 != 0:
        raise InvalidYearCupError(
            {"error": "there was no world cup this year"})

    if year >= 2022:
        raise ImpossibleTitlesError(
            {"error": "impossible to have more titles than disputed cups"})
