from krita import *

def run():
    """Organize layers into categories"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    root = doc.rootNode()
    
    # Scan all layers
    def get_all_nodes(node):
        """Recursively get all nodes"""
        nodes = [node]
        for child in node.childNodes():
            nodes.extend(get_all_nodes(child))
        return nodes
    
    # Category mapping
    def categorize_layer(name):
        name_lower = name.lower()
        
        categories = {
            "BACKGROUND": ["bg", "background", "sky", "cityscape", "landscape"],
            "CHARACTER": ["char", "figure", "portrait", "face", "body"],
            "TECH_DETAILS": ["circuit", "wire", "hud", "interface", "tech"],
            "GLITCH_EFFECTS": ["glitch", "static", "noise", "corrupt", "error"],
            "NEON_OVERLAY": ["neon", "glow", "light", "hologram", "laser"],
            "TEXTURE": ["texture", "grain", "paper", "metal", "concrete"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in name_lower for keyword in keywords):
                return category
        
        return "UNCATEGORIZED"
    
    # Organize layers
    print("📊 Organizing layers...")
    
    all_nodes = get_all_nodes(root)
    layer_count = len(all_nodes)
    
    for node in all_nodes:
        if node.type() == "grouplayer":
            continue
            
        category = categorize_layer(node.name())
        
        # Find or create group for this category
        group = None
        for child in root.childNodes():
            if child.type() == "grouplayer" and child.name() == category:
                group = child
                break
        
        if not group:
            group = doc.createGroupLayer(category)
            root.addChildNode(group, None)
        
        # Move node to group
        parent = node.parentNode()
        if parent and parent != group:
            parent.removeChild(node)
            group.addChildNode(node, None)
    
    print(f"✅ Organized {layer_count} layers into categories")
    print("   • Check layer groups in Layers docker")

# For compatibility
def main():
    run()

def execute():
    run()
