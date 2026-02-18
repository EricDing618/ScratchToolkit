import importlib.util
import sys

def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # 可选：注册到 sys.modules
    spec.loader.exec_module(module)
    return module

# 使用示例
'''my_module = import_from_path("my_module", "/absolute/path/to/module.py")
my_module.some_function()'''

imported = import_from_path("cc", r"D:\gitclone\ScratchToolkit\tests\utils\imported.py")
imported.a()