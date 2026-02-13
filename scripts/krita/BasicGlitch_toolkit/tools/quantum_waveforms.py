from krita import *
import math
import random
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    """Quantum Waveforms: Procedural Interference Pattern Generator"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return
    
    print("🌊 MANIFESTING QUANTUM WAVEFORMS...")
    
    try:
        root = doc.rootNode()
        w = doc.width()
        h = doc.height()
        
        # 1. Create a container group
        group_id = random.randint(1000, 9999)
        group = doc.createGroupLayer(f"FX_Quantum_Waves_{group_id}")
        root.addChildNode(group, None)
        
        empty_selection = Selection()

        # Wave A: The "Carrier" (High Frequency)
        conf1 = InfoObject()
        conf1.setProperty("type", "linear")
        conf1.setProperty("repeat", "alternating")
        conf1.setProperty("color1", QColor(0, 255, 255, 200)) # Cyan
        conf1.setProperty("color2", QColor(0, 0, 0, 0))       # Transparent
        conf1.setProperty("start", QPointF(0, 0))
        conf1.setProperty("end", QPointF(w / 40, h / 40)) 
        
        wave_a = doc.createFillLayer("WAVE: Carrier Frequency", "gradient", conf1, empty_selection)
        wave_a.setBlendingMode("screen")
        group.addChildNode(wave_a, None)
        
        # Wave B: The "Modulator" (Low Frequency, Tilted)
        conf2 = InfoObject()
        conf2.setProperty("type", "linear")
        conf2.setProperty("repeat", "alternating")
        conf2.setProperty("color1", QColor(255, 0, 255, 200)) # Magenta
        conf2.setProperty("color2", QColor(0, 0, 0, 0))
        conf2.setProperty("start", QPointF(0, 0))
        conf2.setProperty("end", QPointF(w / 5, h / 10))
        
        wave_b = doc.createFillLayer("WAVE: Modulator", "gradient", conf2, empty_selection)
        wave_b.setBlendingMode("addition")
        group.addChildNode(wave_b, None)
        
        # Wave C: The "Interference" (Radial)
        conf3 = InfoObject()
        conf3.setProperty("type", "radial")
        conf3.setProperty("repeat", "alternating")
        conf3.setProperty("color1", QColor(255, 255, 0, 150)) # Yellow
        conf3.setProperty("color2", QColor(0, 0, 0, 0))
        conf3.setProperty("start", QPointF(w/2, h/2))
        conf3.setProperty("end", QPointF(w/2 + 100, h/2 + 100))
        
        wave_c = doc.createFillLayer("WAVE: Radial Interference", "gradient", conf3, empty_selection)
        wave_c.setBlendingMode("overlay")
        group.addChildNode(wave_c, None)

        print("   ✅ Quantum Harmonics Manifested.")
        QMessageBox.information(None, "BasicGlitch", 
            "Quantum Waveforms Generated.\n\n"
            "This tool uses overlapping Gradient Recurrence to simulate "
            "mathematical interference patterns.\n\n"
            "Adjust the 'End' point of the Fill Layers to change the frequency!")

    except Exception as e:
        error_msg = f"❌ Waveform Decoherence: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)
    
    doc.refreshProjection()

if __name__ == "__main__":
    run()