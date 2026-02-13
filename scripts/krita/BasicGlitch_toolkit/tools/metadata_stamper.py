from krita import *

def run():
    """Main function called by Krita"""
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No document open")
        return
        
    meta = f"""<document-info>
        <author><full-name>Justin Lance</full-name><url>https://basicglitch.art</url></author>
        <abstract>BasicGlitch Apparel Design - Licensed Product</abstract>
    </document-info>"""
    
    doc.setDocumentInfo(meta)
    print("✅ Metadata Stamped: Justin Lance (BasicGlitch.art)")

if __name__ == "__main__":
    run()
