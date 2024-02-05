import base64
import multiprocessing
from threading import Event
from ...pygrabber.dshow_graph import FilterGraph



class ImgGrab:
    def start(self) -> None:
        self.image = None
        self.event = Event()
        self.graph = FilterGraph()
        self.devices = self.graph.get_input_devices()
        self.graph.add_video_input_device(self.cameraIndex)
        self.graph.add_sample_grabber(self.set_image)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()        
        self.stopped = False

    def set_index(self, index = 0):
        self.cameraIndex = int(index)


    def capture_image(self):
        self.graph.grab_frame()
        while True:
            if self.image != None:
                break
        self.im = self.image
        self.image = None
        return base64.b64encode(bytes(self.im[0])).decode('ascii'), self.im[1]

    def set_image(self, image):
        self.image = image


    def stop(self):
        self.stopped = True
        self.graph.stop()

def _get_available_devices(queue: multiprocessing.Queue):
    graph = FilterGraph()
    queue.put(graph.get_input_devices())

def get_available_devices():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_get_available_devices,args=(queue,))
    p.start()
    p.join()
    return queue.get()

img_grab_obj = ImgGrab()