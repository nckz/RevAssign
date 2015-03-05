/**
	\file decutil.cpp
	\author Nick Zwart
	\date 2011dec31

	\brief c routines for the ISMRM AMPC Reviewer Assignment program 

 **/

#include <Python.h>
#define PY_ARRAY_UNIQUE_SYMBOL DEDUTIL_CPP // must be declared before #include <arrayobject.h>


#include <math.h>   // for sqrt(), log(), and sin(), pow()
#include <time.h>   // for getting sys time to the sec
#include <stdlib.h>
#include <stdio.h>


extern "C"
{
//#include "../globalKernels/io_field.c"
}



/* less than sort function between two item lists
 */
static PyObject *lt_py(PyObject *self, PyObject *args, PyObject *keywds)
{

    /* input list */
    PyObject *list1=NULL;
    PyObject *list2=NULL;
    int col=0;
    int cur_catkey_num=-1;
    int indicator=0;

    /* USER OPTS */
    static char *kwlist[] = {"list1","list2","col","key","indicator", NULL};

    /* get input items, arrays, params, etc... */
    if (!PyArg_ParseTupleAndKeywords(args,keywds,"OOiii",kwlist,&list1,&list2,&col,&cur_catkey_num,&indicator))
    {
        printf("Error: Could not parse input args. (lt_py())\n");
        printf("For more information check %s, line %d\n",__FILE__,__LINE__);
        return NULL;
    }

    //[0:member #, 1:type, 2:first, 3:last, 4:designation, 5:inst., 6:email, 7:training, 8:pubmed, 9:pubmed#, 10:#articles, 11:previously reviewed, 12:choice1, 13:2, 14:3, 15:4, 16:5, 17:#abs, 18:assgnd cat]
    //[0(int),1(str),2(str),3(str),4(str),5(str),6(str),7(str),8(str),9(str),

    /* get items from list */
    PyObject *cur   = PyList_GetItem(list1, col);
    PyObject *other = PyList_GetItem(list2, col);
    int out_logic = 0;

    int match_cur = 0;
    int choice_cur = -1;
    int new_color_cur = 0;
    for(int i=12;i<17;i++)
        if(PyInt_AS_LONG(PyList_GetItem(list1,i)) == cur_catkey_num)
        {
            choice_cur = i;
            new_color_cur = i-11;
            match_cur = 1;
            break; // no need to check the rest
        }

    int match_other = 0;
    int choice_other = -1;
    int new_color_other = 0;
    for(int i=12;i<17;i++)
        if(PyInt_AS_LONG(PyList_GetItem(list2,i)) == cur_catkey_num)
        {
            choice_other = i;
            new_color_other = i-11;
            match_other = 1;
            break; // no need to check the rest
        }

    if(match_cur && match_other)
    {
        if(choice_other == choice_cur)
        {
            // all numeric comparisons
            if((col == 0 ) || (col == 12) || (col == 13) || 
               (col == 14) || (col == 15) || (col == 16) || (col == 17))
                out_logic = PyInt_AS_LONG(cur) < PyInt_AS_LONG(other);
            else // string comparisons
                out_logic = strcmp(PyString_AS_STRING(cur),PyString_AS_STRING(other));
        }
        else
        {
            // sort on choice prio
            if(indicator == 0)
                out_logic = (choice_cur < choice_other);
            else
                out_logic = (choice_cur > choice_other);
        }
    }
    else if(match_cur || match_other)
    {
            // sort on choice prio
            if(indicator == 1)
                out_logic = (choice_cur < choice_other);
            else
                out_logic = (choice_cur > choice_other);
    }
    else
    {
        /* if no choice based matches are found, continue with normal sorting */
        // all numeric comparisons
        if((col == 0 ) || (col == 12) || (col == 13) || 
           (col == 14) || (col == 15) || (col == 16) || (col == 17))
            out_logic = PyInt_AS_LONG(cur) < PyInt_AS_LONG(other);
        else // string comparisons
            out_logic = strcmp(PyString_AS_STRING(cur),PyString_AS_STRING(other));
    }

    /* pack output arrays */
    return Py_BuildValue("iii", out_logic, new_color_cur, new_color_other );
}





/* ##############################################################
 * ##############################################################
 *                  MODULE DESCRIPTION
 * ##############################################################
 * ############################################################## */




/* list of functions to be accessible from python
 */
static PyMethodDef Methods[] = {

    {"lt",(PyCFunction) lt_py, METH_VARARGS|METH_KEYWORDS, // the string is the python accessible name
    "Def: (data) = fft(data)\n\n\
     Brief: fft data in any of six dirs.  The first 1,2 and 3 dirs are threaded.\n\n\
     INPUT (required)\n\
     \t data: (NPY array)\n\
     \t\t KWARGS (optional)\n\
     \t\t s1...s6: (float) scale factor \n\
     \t\t n1...n6: (int) dim length\n\
     \t\t dir: (int) (0:FFTW_FORWARD, 1:FFTW_BACKWARD) (default:0)\n\
     \t\t measureType: (int) fftw 1:ESTIMATE, 2:MEASURE, 3:PATIENT, 4:EXHAUSTIVE (default:1)\n\
     \t\t numThreads: (int) (default: 8)\n\
     \t\t verbosity: (int) >= 0 (default: 0)\n\
     OUTPUT\n\
     \t data: (NPY array)\n\
     "}, // shows up in ipython after ?

    {NULL, NULL, 0, NULL}        /* Sentinel */
};

/* init function that is called at 'import' and 'reload'
 */
PyMODINIT_FUNC initdecutil(void) // <- init<name>
{
    PyObject *m;
    m = Py_InitModule("decutil", Methods); // <- <name>
    if (m == NULL)
    return;

    /* This little guy requires a unique identifier to be declared
     * if multiple extensions are going to comprise the extension
     * module (PY_ARRAY_UNIQUE_SYMBOL).  I don't think this applies
     * to included kernel sources.
     *
     * http://dsnra.jpl.nasa.gov/software/Python/numpydoc/numpy-13.html
     *
     * import_array() is needed if any numpy functions are to be called.
     */
    //import_array();
}
