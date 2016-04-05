import re

from dateutil.parser import parse

class DateRecognizer(object):
    def __init__(self):
        floatDigitPattern = re.compile("-?\d+\.\d+")
        oneDigitPattern = re.compile("^-?\$?\d+$")
        nbspDigitPattern = re.compile("^&nbsp;\d+$")
        pg13Pattern = re.compile("PG-13")
        ps3Pattern = re.compile("^ps3$")
        currencyPattern = re.compile(".*illion.*")
        oneThousandPattern = re.compile("^10\d+")
        aPlusBPattern = re.compile("^\d+\+\d+")
        aMinusBPattern = re.compile("^\d+-\d+")
        self.skipPatterns = [
            floatDigitPattern, oneDigitPattern, pg13Pattern, currencyPattern, nbspDigitPattern, ps3Pattern, oneThousandPattern, aPlusBPattern, aMinusBPattern
        ]

    def isDate(self, string):
        parsedTime = ""

        for pattern in self.skipPatterns:
            if(pattern.match(string)):
                return False

        try:
            parsedTime = parse(string, fuzzy=True)
        except BaseException as e:
            return False

        try:
            if(parsedTime == parse("", fuzzy=True)):
                return False
            else:
                return True
        except:
            return True

if __name__ == "__main__":
    import time
    start_time = time.time()
    dateRecognizer = DateRecognizer()
    import ipdb; ipdb.set_trace()
    for i in range(0, 100000):
        toparse = "10th March %s"%(str(i),)
        dateRecognizer.isDate(toparse)
    print("--- %s seconds ---" % (time.time() - start_time))
