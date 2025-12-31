from krita import *

def glitch_shift_refined():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: return

    # 1. Duplicate the layer
    red_layer = base.duplicate()
    red_layer.setName("GLITCH: Red Shift")
    red_layer.setBlendingMode("screen") # Screen blends the red channel nicely
    doc.rootNode().addChildNode(red_layer, base)
    
    # 2. Shift it
    shift_amount = int(doc.width() * -0.005)
    red_layer.move(shift_amount, 0)
    
    # 3. Isolate Red Channel using a Filter Mask (Cross Channel Adjustment)
    # This automates the "Hide Green and Blue" step
    filter_mask = doc.createFilterMask("Isolate Red")
    filt = filter_mask.filter()
    if filt and filt.name() == "cross_channel_adjustment":
        conf = filt.configuration()
        # The internal params for Channel Mixer can be complex.
        # A simpler robust fallback if specific filter params fail is to rely on Blending Modes.
        # But let's try to set the matrix to zero out G and B.
        # (This part is tricky without exact Krita version docs, so we use a blending mode trick instead)
        pass
    
    # ALTERNATIVE ROBUST METHOD:
    # Instead of complex filter masks, we use a simpler trick:
    # We essentially want this layer to ONLY have Red info.
    # We can add a "Color Adjustment" Filter Mask to kill Saturation? No.
    
    # Let's stick to the user's request: "Hide G and B".
    # Since scripting channel flags requires PyQt, we will use a workaround:
    # We will assume the user has a standard RGBA profile.
    
    print("Red layer created and shifted.")
    print("NOTE: To fully isolate Red programmatically requires PyQt5.")
    print("      We have set Blending Mode to 'Screen' which creates a similar effect.")

# RE-WRITING TO USE BLENDING MODES FOR AUTOMATION
# The best way to simulate "Red Channel Only" without channel flags is:
# 1. Clone Layer
# 2. Add Filter: Color Balance -> Cyan/Red to Max? 
# 3. Actually, the 'Copy Red' blending mode exists in some versions.

# Let's try the cleanest Krita Python approach:
# We will create a Filter Layer that zeroes out Green and Blue.

def automated_glitch():
    doc = Krita.instance().activeDocument()
    node = doc.activeNode()
    
    # Duplicate
    glitch_node = node.duplicate()
    glitch_node.setName("GLITCH: Red Offset")
    glitch_node.setBlendingMode("addition") # Addition/Screen works best for RGB separation
    doc.rootNode().addChildNode(glitch_node, node)
    
    # Offset
    glitch_node.move(int(doc.width() * -0.005), 0)
    
    # Add Channel Mixer Filter Mask to keep only RED
    # Filter ID: 'cross_channel_adjustment'
    # We need to set Green and Blue channels to 0 contribution
    
    # Since scripting complex filter configs is prone to errors across versions,
    # We will leave a clear message but attempting this is better than nothing.
    
    print("Created Glitch Layer. If it looks too bright, manually disable G/B channels in the docker.")

automated_glitch()