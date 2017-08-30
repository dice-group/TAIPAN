"""Utils"""
import re
from dateutil.parser import parse

def clear_string(string):
    string = re.sub('[{}|*?()\[\]!-"]', '', string)
    string = re.sub('&nbsp;', '', string)
    string = string.strip()
    return string

class DateRecognizer(object):
    def __init__(self):
        float_digit_pattern = re.compile("-?\d+\.\d+")
        one_digit_pattern = re.compile("^-?\$?\d+$")
        nbsp_digit_pattern = re.compile("^&nbsp;\d+$")
        pg13_pattern = re.compile("PG-13")
        ps3_pattern = re.compile("^ps3$")
        currency_pattern = re.compile(".*illion.*")
        one_thousand_pattern = re.compile("^10\d+")
        aplusb_pattern = re.compile("^\d+\+\d+")
        aminusb_pattern = re.compile("^\d+-\d+")
        self.skip_patterns = [
            float_digit_pattern, one_digit_pattern, pg13_pattern, currency_pattern, nbsp_digit_pattern, ps3_pattern, one_thousand_pattern, aplusb_pattern, aminusb_pattern
        ]

    def is_date(self, string):
        parsedTime = ""

        for pattern in self.skip_patterns:
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
