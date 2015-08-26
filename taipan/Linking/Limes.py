#import jnius_config
#jnius_config.add_options('-Xrs', '-Xmx4096')
#jnius_config.set_classpath(javaLibFolder)
import os
from jnius import autoclass

from taipan.Config.Pathes import limesClassPath
os.environ["CLASSPATH"] = limesClassPath

from taipan.Config.Pathes import limesExampleXml

class LimesLinker(object):
    def __init__(self):
        pass

    def getController(self):
        Controller = autoclass("de.uni_leipzig.simba.controller.Controller")
        return Controller()

if __name__ == "__main__":
    limesLinker = LimesLinker()
    controller = limesLinker.getController()
    import ipdb; ipdb.set_trace()
