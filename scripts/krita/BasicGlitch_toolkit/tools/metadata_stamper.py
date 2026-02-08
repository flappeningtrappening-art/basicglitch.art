from krita import *

def stamp_refined():
    doc = Krita.instance().activeDocument()
    meta = f"""<document-info>
        <author><full-name>Justin Lance</full-name><url>https://basicglitch.art</url></author>
        <abstract>BasicGlitch Apparel Design - Licensed Product</abstract>
    </document-info>"""
    doc.setDocumentInfo(meta)
    print("Metadata Stamped.")

stamp_refined()
