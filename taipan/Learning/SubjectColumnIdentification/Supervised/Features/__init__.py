from .CellsWithUniqueContentFraction import CellsWithUniqueContentFraction
from .CellsWithNumericContentFraction import CellsWithNumericContentFraction
from .NumberOfWordsAverage import NumberOfWordsAverage
from .NumberOfDigitsAverage import NumberOfDigitsAverage
from .NumberOfLettersAverage import NumberOfLettersAverage
from .Connectivity import Connectivity
from .Support import Support

#FeatureList = [CellsWithUniqueContentFraction(), CellsWithNumericContentFraction(), NumberOfWordsAverage(), NumberOfDigitsAverage(), NumberOfLettersAverage(), Connectivity(), Support()]
FeatureList = [Connectivity(), Support(), CellsWithUniqueContentFraction(), CellsWithNumericContentFraction(), NumberOfDigitsAverage()]
