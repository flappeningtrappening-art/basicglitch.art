from .basicglitch_toolkit import BasicGlitchToolkit
# Only the __init__.py should tell Krita to add the extension
Krita.instance().addExtension(BasicGlitchToolkit(Krita.instance()))