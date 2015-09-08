import os.path
currentDir = os.path.dirname(os.path.realpath(__file__))
tablesDir = "/home/ivan/datahdd/tables"
limesClassPath = os.path.abspath(os.path.join(currentDir, "../../java/libs/limes-core-0.6.4.jar"))
limesExampleXml = os.path.abspath(os.path.join(currentDir, "../../java/limesExamples/dbpedia-dbpedia.xml"))
loggingConfigJson = os.path.abspath(os.path.join(currentDir, "Logging.json"))
