import os
import xml.etree.ElementTree as ET

special_list = {
    "emdash.long.vert": (880, 2000),
    "ellipsis.vert": (806, 818),
    "comma-han.vert": (880, 340),
    "period-han.vert": (880, 290),
    "comma.full.vert": (880, 364),
    "exclam.full.vert": (880, 854),
    "period.full.vert": (880, 253),
    "question.full.vert": (880, 963),
    "colon.full.vert": (880, 553),
    "semicolon.full.vert": (880, 664),
    "endash.vert": (586, 491),
}

default_vert_start = 880
default_vert_height = 1000

path = "./UnboundedSans.ufo/glyphs/"

count=0
for file in os.listdir(path):
    if not file.lower().endswith(".glif"):
        continue

    full_path_name = os.path.join(path, file)
    filename = os.path.splitext(file)[0]

    tree = ET.parse(full_path_name)
    root = tree.getroot()

    #default values
    vert_start = default_vert_start
    vert_height = default_vert_height

    #check if file need override
    if filename in special_list.keys():
        vert_start = special_list[filename][0]
        vert_height = special_list[filename][1]
    
    if len(list(root)) <= 1 and root.find('advance') is None:
        count+=1
        #empty glyph, only has unicode or nothing
        continue

    #set vertical height
    adv = root.find('advance')
    adv.set('height', str(vert_height))

    #add vertical advance
    lib = root.find('lib')
    if lib is None:
        lib = ET.SubElement(root, 'lib')
        dict_ = ET.SubElement(lib, 'dict')
    else:
        dict_ = lib.find('dict')
    key_ = ET.SubElement(dict_, 'key')
    key_.text = "public.verticalOrigin"
    vert_height = ET.SubElement(dict_, 'integer')
    vert_height.text = str(vert_start)

    #print(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(full_path_name, encoding="utf-8", xml_declaration=True)

    #counting
    count+=1
    if count%2500 == 0:
        print("Done %d glyphs." % (count))

print("Total %d glyphs in font." % (count))
