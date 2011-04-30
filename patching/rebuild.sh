
xsltproc --stringparam 'file' web_browsers_patch.xml patch_wurfl.xsl wurfl.xml > wurfl_patched.xml
xsltproc check_wurfl.xsl wurfl_patched.xml

./wurfl2python.py wurfl_patched.xml -o "../src/wurfl.py"
