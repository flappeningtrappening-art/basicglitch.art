from krita import *
import os
import sys
import importlib

# ========================================================
# BASIC GLITCH TOOLKIT - PORTABLE CORE
# ========================================================
# Dynamically loads all tools and registers them in Krita
# ========================================================

class BasicGlitchToolkit(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.tools_path = os.path.join(os.path.dirname(__file__), 'tools')
        if self.tools_path not in sys.path:
            sys.path.insert(0, self.tools_path)
        print(f"[BasicGlitch] Toolkit path initialized: {self.tools_path}")

    def setup(self):
        pass

    def createActions(self, window):
        # Create a top-level menu for the toolkit
        # Note: Krita's Python API for menus is sometimes restricted, 
        # but createAction puts it in the 'Scripts' menu by default.
        
        print("[BasicGlitch] Mapping neural pathways (loading tools)...")
        
        if not os.path.exists(self.tools_path):
            print(f"[BasicGlitch] FATAL: Tools directory not found at {self.tools_path}")
            return

        # Automatically find all .py files in tools/
        for filename in sorted(os.listdir(self.tools_path)):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                action_id = f"bg_{module_name}"
                
                # Friendly name: "quantum_glitch" -> "Quantum Glitch"
                display_name = module_name.replace('_', ' ').title()
                
                try:
                    # Create the action
                    action = window.createAction(action_id, f"BG: {display_name}", "tools/scripts/BasicGlitch")
                    
                    # Connect to the module's run() function
                    # We use a lambda to ensure the correct module is loaded when clicked
                    action.triggered.connect(lambda checked=False, m=module_name: self.run_tool(m))
                    
                    print(f"[BasicGlitch] Registered: {display_name}")
                except Exception as e:
                    print(f"[BasicGlitch] Failed to register {module_name}: {e}")

    def run_tool(self, module_name):
        try:
            # Re-import to allow hot-reloading if you edit the files while Krita is open
            module = importlib.import_module(module_name)
            importlib.reload(module)
            
            # Try different entry points
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()
            elif hasattr(module, 'execute'):
                module.execute()
            else:
                print(f"[BasicGlitch] ERROR: {module_name} has no run() or main() function.")
                
        except Exception as e:
            print(f"[BasicGlitch] ERROR in {module_name}: {e}")
            import traceback
            traceback.print_exc()