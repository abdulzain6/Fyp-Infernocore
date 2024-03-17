#include <windows.h>
#include <Python.h>
int WindowX()//Get the window's X resolution
    {
        RECT desktop_rect_;
        HWND desktop_ = GetDesktopWindow();
        GetWindowRect(desktop_,
                      &desktop_rect_);
        return desktop_rect_.right;
    }

int WindowY()//Get the window's Y resolution
{
    RECT desktop_rect_;
    HWND desktop_ = GetDesktopWindow();
    GetWindowRect(desktop_,
                      &desktop_rect_);
    return desktop_rect_.bottom;
}
void BlockMouseMovement(int block_time) //To block the mouse movement
{
    double seconds_passed = 0;
    while (true) {
        SetCursorPos(WindowX() / 2, WindowY() / 2);
        Sleep(100);
        seconds_passed += 0.1;
        if (seconds_passed > block_time)
            break;
    }

}

void BlockMouse() //To block the mouse movement
{
    while (true) {
        SetCursorPos(WindowX() / 2, WindowY() / 2);
        Sleep(0.0001);
    }

}
static PyObject* _blockMouseSeconds(PyObject* self, PyObject *args) {
    int secs;
    if (!PyArg_ParseTuple(args, "i", &secs))
        return NULL;
    BlockMouseMovement(secs);
	return Py_BuildValue("i", 1);
}
static PyObject* _blockMouse(PyObject* self) {
    BlockMouse();
	return Py_BuildValue("i", 1);
}

static struct PyMethodDef methods[] = {
	{"blockMouseSeconds" , (PyCFunction)_blockMouseSeconds, METH_VARARGS},
  	{"blockMouse" , (PyCFunction)_blockMouse, METH_NOARGS},

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