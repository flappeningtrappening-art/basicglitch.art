from krita import Krita, Extension
from PyQt5.QtWidgets import QMenu, QAction
import sys

class GlitchFix(Extension):
    def __init__(self, parent): 
        super().__init__(parent)
    
    def setup(self): 
        pass
    
    def createActions(self, window):
        menu = QMenu("&Glitch Tools", window.qwindow().menuBar())
        window.qwindow().menuBar().addMenu(menu)
        
        tools = [("Fractured Mirror", "fractured_mirror"),
                 ("RGB Glitch", "rgb_glitch"),
                 ("Neon Glow", "neon_glow"),
                 ("Circuit Grid", "circuit_grid"),
                 ("Kaleidoscope", "kaleidoscope_symmetry")]
        
        for name, module in tools:
            action = QAction(name, menu)
            action.triggered.connect(lambda _, m=module: self.run_tool(m))
            menu.addAction(action)
        print("Glitch Tools menu created")
    
    def run_tool(self, module):
        from krita import Krita
        if not Krita.instance().activeDocument():
            print("Open a document first")
            return
        
        path = r'C:\Program Files\Krita (x64)\share\krita\pykrita\BasicGlitch_toolkit\tools'
        if path not in sys.path: 
            sys.path.append(path)
        
        try:
            __import__(module).run()
        except Exception as e:
            print(f"Error: {e}")

Krita.instance().addExtension(GlitchFix(Krita.instance()))
