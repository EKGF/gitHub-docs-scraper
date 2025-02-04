import os
import sys

if not __package__:
    # Make CLI runnable from source tree with `python src/scraper`
    package_src_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_src_path)
