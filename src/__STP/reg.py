from .codeparser import *

class CodeParser(CodeParser):
    def add(self):
        super().add()
        match self.opcode: #匹配相应的积木名
            case "control_wait":
                self.sleep=True
                self.fstr(args=(self.idinfo['inputs']['DURATION'][1][1]))
            case "control_repeat":
                '''self.fstr(f"for _ in range({self.idinfo['inputs']['TIMES'][1][1]}):",3)'''
            case "control_forever":
                self.fstr("while True:",3)
            case "control_if":
                self.funccode['__init__'][1][f"id={self.id}"]=self.depth
                self.fstr(args=())
                '''self.fstr(f"if {self.idinfo['inputs']['CONDITION'][1][1]}:",3)'''
            case "control_if_else":
                '''self.fstr(f"if {self.idinfo['inputs']['CONDITION'][1][1]}:",3)'''
                self.fstr("else:",3)
            case "operator_add":
                self.fstr(args=["NUM",'+'],mode=6)
            case "operator_subtract":
                self.fstr(args=["NUM",'-'],mode=6)
            case "operator_equals":
               self.fstr(args=["OPERAND",'=='],mode=6)
            case "procedures_definition":
                self.fstr(self.blocks[self.idinfo['inputs']['custom_block'][1]]['mutation'],1)
            case _:
                if self.opcode not in USERSET["blocks"]['ignore']:
                    log.warning(f'Unknown id "{self.opcode}"!')