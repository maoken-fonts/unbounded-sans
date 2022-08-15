@echo OFF

echo === Moving font name... ====
:: move correct name into folder
echo f | xcopy /f /y .\fontinfo.plist .\UnboundedSans.ufo\fontinfo.plist

:: generate final font
echo === Generating static font... ====
fontmake -u .\UnboundedSans.ufoz --overlaps-backend pathops --output-dir "../fonts/" -o ttf otf

:: fix CFF table
echo === Fixing CFF table... ===
py cff_cid_key.py ../fonts/UnboundedSans.otf
