#include <windows.h>
#include <Python.h>


typedef VOID ( _stdcall
               *RtlSetProcessIsCritical ) ( //To set process critical.
                   IN BOOLEAN
                   NewValue,
                   OUT PBOOLEAN
                   OldValue, // (optional)
                   IN BOOLEAN
                   IsWinlogon );

BOOL EnablePriv(LPCSTR lpszPriv) { // Needed to make process critical.
	HANDLE hToken;
	LUID luid;
	TOKEN_PRIVILEGES tkprivs;
	ZeroMemory(&tkprivs, sizeof(tkprivs));

	if (!OpenProcessToken(GetCurrentProcess(), (TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY), &hToken))
		return FALSE;

	if (!LookupPrivilegeValue(NULL, lpszPriv, &luid)) {
		CloseHandle(hToken);
		return FALSE;
	}

	tkprivs.PrivilegeCount = 1;
	tkprivs.Privileges[0].Luid = luid;
	tkprivs.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

	BOOL bRet = AdjustTokenPrivileges(hToken, FALSE, &tkprivs, sizeof(tkprivs), NULL, NULL);
	CloseHandle(hToken);
	return bRet;
}


int ProtectProcess() { // To make the process Critical.
	HANDLE hDLL;
	RtlSetProcessIsCritical fSetCritical;

	hDLL = LoadLibraryA("ntdll.dll");
	if (hDLL != NULL) {
		EnablePriv(SE_DEBUG_NAME);
		(fSetCritical) = (RtlSetProcessIsCritical) GetProcAddress((HINSTANCE) hDLL, "RtlSetProcessIsCritical");
		if (!fSetCritical) return 0;
		fSetCritical(1, 0, 0);
		return 1;
	} else
		return 0;
}

int UnProtectProcess() { // To make the process unCritical.
	HANDLE hDLL;
	RtlSetProcessIsCritical fSetCritical;

	hDLL = LoadLibraryA("ntdll.dll");
	if (hDLL != NULL) {
		EnablePriv(SE_DEBUG_NAME);
		(fSetCritical) = (RtlSetProcessIsCritical) GetProcAddress((HINSTANCE) hDLL, "RtlSetProcessIsCritical");
		if (!fSetCritical) return 0;
		fSetCritical(0, 0, 0);
		return 1;
	} else
		return 0;
}
int IsProcessElevated() { //To check if process is running elevated or not (Run as admin)
	BOOL fIsElevated = 0;
	HANDLE hToken = NULL;
	TOKEN_ELEVATION elevation;
	DWORD dwSize;

	if (!OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken)) {
		goto Cleanup;  // if Failed, we treat as False
	}


	if (!GetTokenInformation(hToken, TokenElevation, &elevation, sizeof(elevation), &dwSize)) {
		goto Cleanup;// if Failed, we treat as False
	}

	fIsElevated = elevation.TokenIsElevated;

Cleanup:
	if (hToken) {
		CloseHandle(hToken);
		hToken = NULL;
	}
	return fIsElevated;
}



L


static PyObject* _isElevated(PyObject* self) {
	return Py_BuildValue("i", IsProcessElevated());
}

static PyObject* _protectProcess(PyObject* self) {
	return Py_BuildValue("i", ProtectProcess());
}
static PyObject* _UnprotectProcess(PyObject* self) {
	return Py_BuildValue("i", UnProtectProcess());
}

static struct PyMethodDef methods[] = {
	{"isElevated" , (PyCFunction)_isElevated, METH_NOARGS},
	{"protectProcess" , (PyCFunction)_protectProcess, METH_NOARGS},
	{"unProtectProcess" , (PyCFunction)_UnprotectProcess, METH_NOARGS},

	{NULL,NULL}
};

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"processManagement",
	NULL,
	-1,
	methods
};

PyMODINIT_FUNC PyInit_processManagement(void){
	return PyModule_Create(&module);
}