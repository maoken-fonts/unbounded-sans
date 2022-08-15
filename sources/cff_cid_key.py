import copy
from fontTools import ttLib
from fontTools.cffLib import (
    FDArrayIndex,
    FontDict,
    FDSelect,
)
import sys

fontfile = sys.argv[1]

font = ttLib.TTFont(fontfile)
glyphOrder = font.getGlyphOrder()

cff = font["CFF "].cff.values()[0]
fontName = font["CFF "].cff.keys()[0]

cff.ROS = ("Adobe", "Identity", 0)

# delete encoding when converting to CID-keyed
del cff.rawDict["Encoding"]
mapping = {
    name: ("cid" + str(n) if n else ".notdef") for n, name in enumerate(cff.charset)
}
charstrings = cff.CharStrings
charstrings.charStrings = {
    mapping[name]: v for name, v in charstrings.charStrings.items()
}
cff.charset = ["cid" + str(n) if n else ".notdef" for n in range(len(cff.charset))]


# sample from https://github.com/fonttools/fonttools/blob/21d22ae30f88b76fab5575f5f2e882b142ee1c08/Lib/fontTools/varLib/cff.py#L64
if not hasattr(cff, "FDArray"):
    # format 3 FDSelect
    cff.FDSelect = FDSelect(None, None, 3)

    # create FDArray
    fdArray = cff.FDArray = FDArrayIndex()
    fdArray.strings = None
    fdArray.GlobalSubrs = cff.GlobalSubrs
    cff.GlobalSubrs.fdArray = fdArray
    if charstrings.charStringsAreIndexed:
        charstrings.charStringsIndex.fdArray = fdArray
    else:
        charstrings.fdArray = fdArray

    # set FDSelectIndex = 0 for every T2CharString in GlobalSubrs
    for item in charstrings.keys():
        charstrings[item].fdSelectIndex = 0

    # create FontDict in FDArray
    fontDict = FontDict()  # default index 0
    fdArray.append(fontDict)
    # generate fontdict name
    fontDict.FontName = fontName + "-All"

    # add Private from CFF topDict into FontDict
    fontDict.Private = copy.deepcopy(cff.Private)

    # remove Private from CFF topDict
    # cff.Private = None
    del cff.Private
    del cff.rawDict["Private"]

font.save(fontfile, reorderTables=False)
