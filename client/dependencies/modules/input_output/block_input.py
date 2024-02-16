from ctypes import wintypes
import mouseBlock, processManagement, ctypes, time

class BlockInput:
    def __init__(self) -> None:
        self.BlockInput = ctypes.windll.user32.BlockInput
        self.BlockInput.argtypes = [wintypes.BOOL]
        self.BlockInput.restype = wintypes.BOOL
        self.secondsPassed = 0
    
    def block_all_seconds(self, seconds):
        """Blocks all input for the seconds provided."""
        blocked = self.block_all()
        if blocked:
            time.sleep(seconds)
            self.unblock_all()
        return blocked

    def block_all(self):
        """Blocks all input"""
        return self.BlockInput(True) if processManagement.isElevated() == 1 else 0

    def unblock_all(self):
        """unBlocks all input"""
        return self.BlockInput(False) if processManagement.isElevated() == 1 else 0

    def block_mouse_seconds(self, seconds):
        """Blocks mouse for seconds given"""
        mouseBlock.blockMouseSeconds(seconds)

    def block_mouse(self):
        import multiprocessing
        self.proc = multiprocessing.Process(target = mouseBlock.blockMouse, args = ())
        self.proc.start()

    def unblock_mouse(self):
        self.proc.terminate()

    def block_smart_seconds(self, seconds):
        if processManagement.isElevated() == 1:
            self.block_all_seconds(seconds)
        else:
            self.block_mouse_seconds(seconds)

block_input_obj = BlockInput()