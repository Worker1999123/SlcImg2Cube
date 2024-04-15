from src.d3.model import tools as mt
def STLtoOFF(import_path, output_path):
    up_conversion = None
    result = mt.convert(import_path, output_path, up_conversion)
    with open(output_path, 'w') as f:
        f.write(result)