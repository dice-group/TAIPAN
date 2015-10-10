import foxpy.fox

class FoxIdentifier(object):
    def __init__(self):
        pass

    def identifyEntity(self, columnValue, headerValue):
        """
            FOX requires a full sentence to recognize entities. Could possibly work for some of the values inside the tables, which contain sentences (e.g. Notes).

            Here we try to concat columnvalue with headervalue thus recreating something like Hearst pattern from a table.
        """
        fx = foxpy.fox.Fox()
        (text, output, log) = fx.recognizeText(
                self.clearString(headerValue) + ' ' + self.clearString(columnValue))
        entity = re.search("\"(dbpedia:.*)\"", output)
        if(entity):
            entity = entity.group(1)
            entity = re.sub('dbpedia:', "http://dbpedia.org/resource/", entity)
            return entity
        else:
            return ""

    def clearString(self, string):
        characters = "{}|"
        string = string.translate(None, characters)
        string = re.sub('&nbsp;', '', string)
        string = string.strip()
        return string

if __name__ == "__main__":
    foxIdentifier = FoxIdentifier()
    print foxIdentifier.identifyEntity("Austria", "Country")
