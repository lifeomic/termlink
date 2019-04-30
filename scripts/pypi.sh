#!/bin/bash
make package
pip install twine 
python -m twine upload dist/*