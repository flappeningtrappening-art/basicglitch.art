from krita import *
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
import os
import sys
import importlib
import traceback

# ========================================================
# QUANTUM LOADER: BASIC GLITCH TOOLKIT
# ========================================================
# Strategy: Simultaneous Path Exploration
# 1. Attempts standard Krita action factory.
# 2. Attempts direct QMenu injection.
# 3. Validates pathing via relative location (universal).
# 4. Isolates individual tool failures to prevent total collapse.
# ========================================================

class BasicGlitchToolkit(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        # Quantum State 1: Location Agnostic
        self.toolkit_root = os.path.dirname(os.path.realpath(__file__))
        self.tools_path = os.path.join(self.toolkit_root, 'tools')
        
        # Inject into system path immediately
        if self.tools_path not in sys.path:
            sys.path.append(self.tools_path)

    def setup(self):
        pass

    def createActions(self, window):
        """
        The Observation Event.
        Tries to manifest the menu into reality.
        """
        # Quantum State 2: UI Injection Vectors
        # We try to create a dedicated menu first.
        try:
            action_manager = Krita.instance().action("tools_scripts")
            if not action_manager:
                # Fallback Vector: Create top-level menu if Scripts missing
                menu_bar = window.qwindow().menuBar()
                self.custom_menu = menu_bar.addMenu("BasicGlitch")
            else:
                self.custom_menu = None # We will use standard actions
                
            self.load_tools(window)
            
        except Exception as e:
            self.quantum_collapse(f"Menu Creation Failed: {e}")

    def load_tools(self, window):
        if not os.path.exists(self.tools_path):
            self.quantum_collapse(f"Critical: Tools path void: {self.tools_path}")
            return

        loaded_count = 0
        
        # Quantum State 3: Parallel Module Iteration
        for filename in sorted(os.listdir(self.tools_path)):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                
                try:
                    # Entangle the module
                    # We use standard import logic but wrapped in isolation field
                    module = importlib.import_module(module_name)
                    importlib.reload(module)
                    
                    # Identify Entry Point
                    run_func = None
                    if hasattr(module, 'run'): run_func = module.run
                    elif hasattr(module, 'main'): run_func = module.main
                    
                    if run_func:
                        # Manifest Action
                        action_name = f"bg_{module_name}"
                        text_name = module_name.replace('_', ' ').title()
                        
                        action = window.createAction(action_name, f"BG: {text_name}", "tools/scripts/BasicGlitch")
                        action.triggered.connect(lambda c=False, f=run_func: self.safe_execute(f))
                        
                        loaded_count += 1
                        
                except Exception as e:
                    # Non-fatal decoherence. Log it but continue loading others.
                    print(f"[BG_Quantum] Failed to load {module_name}: {e}")

        if loaded_count == 0:
            self.quantum_collapse("Zero tools loaded. Directory scan returned no valid modules.")

    def safe_execute(self, func):
        """Executes tool within a safety containment field"""
        try:
            func()
        except Exception as e:
            QMessageBox.critical(None, "Basic Glitch Runtime Error", f"Tool crashed:\n{e}\n\n{traceback.format_exc()}")

    def quantum_collapse(self, reason):
        """
        Total System Failure.
        Materializes a message box directly to user.
        """
        err_msg = f"BASIC GLITCH TOOLKIT LOAD FAILURE\n\n{reason}\n\nPath: {self.tools_path}\n\nTraceback:\n{traceback.format_exc()}"
        print(err_msg)
        try:
            QMessageBox.warning(None, "Quantum Loader Error", err_msg)
        except:
            pass

# Initialize Extension
Krita.instance().addExtension(BasicGlitchToolkit(Krita.instance()))