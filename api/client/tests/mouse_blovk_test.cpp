#include <Python.h>

// Platform-specific includes
#ifdef _WIN32
#include <windows.h>
#else
#ifdef __linux__
#include <X11/Xlib.h>
#include <unistd.h>
#include <stdlib.h>
#else
#ifdef __APPLE__
#include <ApplicationServices/ApplicationServices.h>
#endif
#endif
#endif

static void MoveCursorToCenter() {
#ifdef _WIN32
    int x = GetSystemMetrics(SM_CXSCREEN) / 2;
    int y = GetSystemMetrics(SM_CYSCREEN) / 2;
    SetCursorPos(x, y);
#elif defined(__linux__)
    Display *display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "Cannot open display\n");
        exit(1);
    }
    int screen = DefaultScreen(display);
    Window root = RootWindow(display, screen);
    int x = DisplayWidth(display, screen) / 2;
    int y = DisplayHeight(display, screen) / 2;
    XWarpPointer(display, None, root, 0, 0, 0, 0, x, y);
    XFlush(display);
    XCloseDisplay(display);
#elif defined(__APPLE__)
    CGEventRef move = CGEventCreateMouseEvent(
        NULL, kCGEventMouseMoved,
        CGPointMake(CGDisplayPixelsWide(CGMainDisplayID()) / 2,
                    CGDisplayPixelsHigh(CGMainDisplayID()) / 2),
        kCGMouseButtonLeft // ignored
    );
    CGEventPost(kCGHIDEventTap, move);
    CFRelease(move);
#endif
}

static void BlockMouseMovement(int block_time) {
    double start_time = clock();
    while ((clock() - start_time) / CLOCKS_PER_SEC < block_time) {
        MoveCursorToCenter();
#ifdef _WIN32
        Sleep(10); // Using Sleep on Windows, sleep time is in milliseconds
#else
        usleep(10000); // Using usleep on Linux/macOS, sleep time is in microseconds
#endif
    }
}

static PyObject* _blockMouseSeconds(PyObject* self, PyObject *args) {
    int secs;
    if (!PyArg_ParseTuple(args, "i", &secs))
        return NULL;
    BlockMouseMovement(secs);
    return Py_BuildValue("i", 1);
}



static struct PyMethodDef methods[] = {
	{"blockMouseSeconds" , (PyCFunction)_blockMouseSeconds, METH_VARARGS},
	{NULL,NULL}
};

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"mouseBlock",
	NULL,
	-1,
	methods
};

PyMODINIT_FUNC PyInit_mouseBlock(void){
	return PyModule_Create(&module);
}