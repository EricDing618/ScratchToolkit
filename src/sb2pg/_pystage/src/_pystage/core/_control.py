from pystage.core._base_sprite import BaseSprite

class _Control(BaseSprite):

    def __init__(self):
        super().__init__()

    def control_wait(self, secs):
        self.code_manager.current_block.add_to_wait_time = secs

    def control_stop_all(self):
        for s in self.stage.sprites:
            s.code_manager.stop_running_blocks()
        self.stage.code_manager.stop_running_blocks()

    control_stop_all.opcode="control_stop"
    control_stop_all.param="STOP_OPTION"
    control_stop_all.value="all"

    def control_stop_this(self):
        self.code_manager.stop_running_blocks()

    control_stop_this.opcode="control_stop"
    control_stop_this.param="STOP_OPTION"
    control_stop_this.value="this script"

    def control_stop_other(self):
        for s in self.stage.sprites:
            if s is not self:
                s.code_manager.stop_running_blocks()
        self.stage.code_manager.stop_running_blocks()

    control_stop_other.opcode="control_stop"
    control_stop_other.param="STOP_OPTION"
    control_stop_other.value="other scripts in sprite"

    # Cloning is probably tricky.  
    def control_create_clone_of_sprite(self, sprite):
        print("Creating a clone of ", sprite)
        sprite._core.clone()

    control_create_clone_of_sprite.opcode = "control_create_clone_of"

    
class _ControlSprite(_Control):

    number_of_clones = 0

    def __init__(self):
        super().__init__()

    def control_create_clone_of_myself(self):
        print("Creating a clone of myself")
        self._core.clone()

    control_create_clone_of_myself.opcode="control_create_clone_of"
    control_create_clone_of_myself.param="CLONE_OPTION"
    control_create_clone_of_myself.value="_myself_"

    def control_delete_this_clone(self):
        _ControlSprite.number_of_clones -= 1
        self.kill()
        self.code_manager.stop_running_blocks()
    control_delete_this_clone.translation = "control_deletethisclone"


    # This is actually an event but Scratch has the hat block under "Control"
    def control_start_as_clone(self, generator_function, name="", no_refresh=False):
        '''
        Adds the code block to the event queue for clicks.
        '''
        new_block = self.code_manager.register_code_block(generator_function, name, no_refresh)
        self.code_manager.cloned_blocks.append(new_block)
        print(f"Bound to start as clone: {new_block.name}")
    control_start_as_clone.translation = "control_startasclone"

    def clone(self):
        # In Scratch, there can only be a maximum of 300 Clones
        if _ControlSprite.number_of_clones >= 300:
            return
        _ControlSprite.number_of_clones += 1
        clone = self.stage._core.pystage_createsprite()._core
        clone.is_clone = True
        # All cloned by reference, be careful where this matters
        cloned_attributes = [
            # Motion
            "_direction", "draggable", 
            # Pen
            "pen", "pen_color", "pen_size", "old_position", "pen_up_at",
            # Looks
            "size", "ghost", "visible",
            # Sound
            "sound_manager", "current_pan", "current_pitch", "current_volume", 
            ]
        for attr in cloned_attributes:
            setattr(clone, attr, getattr(self, attr))
        # copy position over
        clone._pos.x = self._pos.x
        clone._pos.y = self._pos.y
        # clones have own variables 
        clone.variables = self.variables.copy()
        # But only the original variable can be monitored.
        # However, monitors can be shown and hidden, so we need access
        clone.monitors = self.monitors
        
        # Costumes
        clone.costume_manager.costumes = self.costume_manager.costumes
        clone.costume_manager.current_costume = self.costume_manager.current_costume
        clone.costume_manager.rotation_style = self.costume_manager.rotation_style

        # Code
        clone.code_manager = self.code_manager.clone(clone)
        for code_block in clone.code_manager.cloned_blocks:
            code_block.start_or_restart()