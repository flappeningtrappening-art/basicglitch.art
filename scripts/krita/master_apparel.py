from krita import *

def create_apparel_master_templates():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("Please open a document first!")
        return
    
    res = doc.xRes()
    root = doc.rootNode()
    
    templates = {
        "HOODIE / SHIRT": (12, 16),
        "BACKPACK (Main Panel)": (10, 12),
        "BANDANA (Full)": (22, 22),
        "TOTE BAG": (12, 12),
        "SOCKS (Leg Zone)": (3.5, 4.5),
        "BEANIE (Sock Hat)": (4, 2.5),
        "BALL CAP (Front Logo)": (4, 2)
    }
    
    group = doc.createGroupLayer("APPAREL DESIGN GUIDES")
    root.addChildNode(group, None)
    
    for name, dimensions in templates.items():
        w_in, h_in = dimensions
        info = InfoObject()
        info.setProperty("color", "#00fff7") 
        layer = doc.createFillLayer(f"GUIDE: {name}", "color", info)
        layer.setOpacity(40) 
        layer.setVisible(False) 
        group.addChildNode(layer, None)

    print("[COMPLETE] Toggle guides in the 'APPAREL DESIGN GUIDES' group!")

create_apparel_master_templates()
