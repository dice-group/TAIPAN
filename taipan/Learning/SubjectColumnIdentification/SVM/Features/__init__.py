from .CellsWithUniqueContentFraction import CellsWithUniqueContentFraction
from .CellsWithNumericContentFraction import CellsWithNumericContentFraction
from .NumberOfWordsAverage import NumberOfWordsAverage
from .NumberOfDigitsAverage import NumberOfDigitsAverage
from .NumberOfLettersAverage import NumberOfLettersAverage

FeatureList = [CellsWithUniqueContentFraction(), CellsWithNumericContentFraction(), NumberOfWordsAverage(), NumberOfDigitsAverage(), NumberOfLettersAverage()]
