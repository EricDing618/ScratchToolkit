# Online Converter, URL: http://localhost:8000/conversion/823S3-YfcV7
# clone_test (pyStage, converted from Scratch 3)

from pystage.en import Sprite, Stage
import random

stage = Stage()

sprite1 = stage.add_a_sprite()

def when_program_starts_1(self):
    for _ in range(10):
        self.create_clone_of_myself()
        self.create_clone_of_sprite(sprite1)

sprite1.when_program_starts(when_program_starts_1)

def when_i_start_as_a_clone_2(self):
    self.go_to_random_position()
    self.wait(random.randrange(3))
    self.delete_this_clone()

sprite1.when_i_start_as_a_clone(when_i_start_as_a_clone_2)


stage.play()
