from taipan.T2D.Sampler import T2DSampler

t2dSampler = T2DSampler()
tables = t2dSampler.getTables()

withoutAnyProperties = 0
withClassThing = 0
onlyOneKeyProperty = 0
noKeyProperty = 0
noClasses = 0

for table in tables:
    properties = table.properties
    propertiesLength = len(properties)

    if propertiesLength == 0:
        withoutAnyProperties += 1

    hasKeyProperty = False
    for _property in properties:
        if _property['isKey'] == True:
            hasKeyProperty = True

    if hasKeyProperty == True and propertiesLength == 1:
        onlyOneKeyProperty += 1

    if hasKeyProperty == False and propertiesLength > 0:
        noKeyProperty += 1

    classes = table.classes
    classesLength = len(classes)
    for _class in classes:
        if _class['uri'] == 'http://www.w3.org/2002/07/owl#Thing':
            withClassThing += 1

    if classesLength == 0:
        noClasses += 1

print "total: %s" %(len(tables),)
print "withoutAnyProperties: %s" %(withoutAnyProperties,)
print "withClassThing: %s" %(withClassThing,)
print "onlyOneKeyProperty: %s" %(onlyOneKeyProperty,)
print "noKeyProperty: %s" %(noKeyProperty,)
print "noClasses: %s" %(noClasses,)

import ipdb; ipdb.set_trace()
