#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Function 1: A simple 'hello world' function
static PyObject* helloworld(PyObject* self, PyObject* args)
{
    printf("Hello World 3\n");
    return Py_None;
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef
myMethods[] = {
    { "helloworld", helloworld, METH_NOARGS, "Prints Hello World" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef
HelloWorldModule = {
    PyModuleDef_HEAD_INIT,
    "HelloWorldModule",
    "Test Module",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC
PyInit_HelloWorldModule(void)
{
    return PyModule_Create(&HelloWorldModule);
}
