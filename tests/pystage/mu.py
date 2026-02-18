# mu.sb3 -> mu.py (pyStage, converted from Scratch 3)

from pystage.en import Sprite, Stage

stage = Stage()
stage.add_backdrop('splash')
stage.pystage_addsound('his_theme')
stage.create_variable('间距')
stage.create_variable('数量')
stage.create_variable('遍历编号')

def when_GREENFLAG_clicked_1(self):
    while True:
        self.play_sound_until_done("his_theme")

stage.when_GREENFLAG_clicked(when_GREENFLAG_clicked_1)

# Create and initialize sprite '_1'
_1 = stage.add_a_sprite(None)
_1.set_name("角色1")
_1.set_x(125)
_1.set_y(6)
_1.go_to_back_layer()
_1.go_forward(1)
_1.hide()
_1.add_costume('_1', center_x=0, center_y=0)

# Scratch Blocks for '_1'

def when_program_starts_2(self):
    "NO TRANSLATION: procedures_call"
    while True:
        self.erase_all()
        "NO TRANSLATION: procedures_call"

_1.when_program_starts(when_program_starts_2)

stage.play()
