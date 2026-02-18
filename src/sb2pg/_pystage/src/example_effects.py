from pystage.en import Sprite, Stage

stage = Stage()
# Create and initialize sprite 'sprite1'
sprite1 = stage.add_a_sprite()
sprite1.set_name("Sprite1")
sprite1.set_x(-168)
sprite1.set_y(110)

# Create and initialize sprite 'cat'
cat = stage.add_a_sprite()
cat.set_name("Cat")
cat.set_x(-129)
cat.set_y(-123)

# Create and initialize sprite 'cat2'
cat2 = stage.add_a_sprite()
cat2.set_name("Cat2")
cat2.set_x(134)
cat2.set_y(105)

# Create and initialize sprite 'cat3'
cat3 = stage.add_a_sprite()
cat3.set_name("Cat3")
cat3.set_x(148)
cat3.set_y(-112)

# Create and initialize sprite 'cat4'
cat4 = stage.add_a_sprite()
cat4.set_name("Cat4")
cat4.set_x(-152)
cat4.set_y(-11)

# Create and initialize sprite 'cat5'
cat5 = stage.add_a_sprite()
cat5.set_name("Cat5")
cat5.set_x(-4)
cat5.set_y(-117)

# Create and initialize sprite 'cat6'
cat6 = stage.add_a_sprite()
cat6.set_name("Cat6")
cat6.set_x(-11)
cat6.set_y(97)

# Scratch Blocks for 'sprite1'

def when_program_starts_1(self):
    self.set_color_effect_to(100.0)

sprite1.when_program_starts(when_program_starts_1)

# Scratch Blocks for 'cat'

def when_program_starts_2(self):
    self.set_fisheye_effect_to(100.0)

cat.when_program_starts(when_program_starts_2)

# Scratch Blocks for 'cat2'

def when_program_starts_3(self):
    self.set_whirl_effect_to(200.0)

cat2.when_program_starts(when_program_starts_3)

# Scratch Blocks for 'cat3'

def when_program_starts_4(self):
    self.set_pixelate_effect_to(100.0)

cat3.when_program_starts(when_program_starts_4)

# Scratch Blocks for 'cat4'

def when_program_starts_5(self):
    self.set_mosaic_effect_to(24.0)

cat4.when_program_starts(when_program_starts_5)

# Scratch Blocks for 'cat5'

def when_program_starts_6(self):
    self.set_brightness_effect_to(50.0)

cat5.when_program_starts(when_program_starts_6)

# Scratch Blocks for 'cat6'

def when_program_starts_7(self):
    self.set_ghost_effect_to(50.0)

cat6.when_program_starts(when_program_starts_7)

stage.play()

