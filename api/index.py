import sys
import os

# Add the root directory to Python path so that 'backend' module is recognized
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.app.main import app
