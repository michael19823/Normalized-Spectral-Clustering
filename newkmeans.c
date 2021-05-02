#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>

typedef struct {
    double size;
    double* sum;
    double* cent;
}cluster;

void add_to_sum(cluster* cluster, double* to_add, int dim);
void dec_from_sum(cluster* cluster, double* to_add, int dim);
void calc_cen(cluster* cluster, int dim);
int find_min(double* singob, cluster* cluster_arr, int k, int d);
int check_eq(double* before, double* after, int d);
void print_cen(cluster* cluster_arr, int k, int d);
static PyObject* calkmeans(PyObject *self, PyObject *args);
static void starter(PyObject * list, Py_ssize_t list_size, int* k, int* n, int* d, int* max);
static bool starter2(PyObject * list, Py_ssize_t list_size, double* indarr);
static bool starter3(PyObject * list, Py_ssize_t list_size, int j, double** obs_arr);
PyObject *make_list(long * array, Py_ssize_t size);

//*function called from SpectralClusterin, return n size list where every index i represents the cluster that observation i was assigend to.
static PyObject* calkmeans(PyObject *self, PyObject *args)
{
    PyObject *_list, *item, *torett;
    Py_ssize_t a, b;
    cluster* cluster_arr;
    double** obs_arr;
    double* cluster_arr_index;
    int k, n, d;
    int max_iter;
    int i,j,l,m,c,count,z;
    long* indexx;
    long pp;
    long jnk;
    cluster jnkclus;
    double jnk_double;

    //junk values to avoid build compiletion warnings.
    jnk_double=2.00;
    cluster_arr_index=&jnk_double;
    obs_arr=&cluster_arr_index;


    cluster_arr=&jnkclus;
    max_iter=k=d=n=count=2;
    jnk=2;
    indexx=&jnk;
    if(!PyArg_ParseTuple(args, "O:print_int_lists", &_list)) {
        return NULL;
    }
    /* Is it a list? */
    if (!PyList_Check(_list))
        return NULL;

    b = PyList_Size(_list);  /*  Same as in Python len(_list)  */
    /* Go over each item of the list and reduce it */
    for (a = 0; a < b; a++) {
        item = PyList_GetItem(_list, a);
        if (!PyList_Check(item)){  /* We only print lists */
            continue;
        }
        if(a==0){
            starter(item, PyList_Size(item), &k, &n , &d, &max_iter);
            if(k>=n){
                printf("wrong");
                return 0;}
            indexx = calloc(n, sizeof(long));
            if(indexx==NULL){
                printf("fail to allocate memory");
                exit(0);
            }
            obs_arr = calloc(n, sizeof(double*));
            if(obs_arr==NULL){
                printf("fail to allocate memory");
                free(indexx);
                exit(0);
            }
            cluster_arr_index = calloc(k, sizeof(double));
            if(cluster_arr_index==NULL){
                printf("fail to allocate memory");
                free(indexx);
                free(obs_arr);
                exit(0);
            }

            for(i=0;i<n;i++){
                obs_arr[i]=calloc(d,sizeof(double));
            if(obs_arr[i]==NULL){
                printf("fail to allocate memory");
                free(indexx);
                free(obs_arr);
                free(cluster_arr_index);
                exit(0);
            }
            }
            cluster_arr = calloc(k, sizeof(cluster));
            if (cluster_arr == NULL){
                printf("fail to allocate memory");
                free(indexx);
                free(cluster_arr_index);
                for(i=0;i<n;i++){
                    free(obs_arr[i]);
                }
                free(obs_arr);
                exit(0);
            }
            for(i=0;i<k;i++){
                cluster_arr[i].cent=calloc(d,sizeof(double));
                cluster_arr[i].sum=calloc(d,sizeof(double));

        if (cluster_arr[i].cent==NULL || cluster_arr[i].sum==NULL){
            printf("fail to allocate memory");
            free(cluster_arr_index);
            free(indexx);
            for(i=0;i<n;i++){
                    free(obs_arr[i]);
                }
            free(obs_arr);
            free(cluster_arr);
            exit(0);
            }
            }
        }
        if(a==1){if(starter2(item, PyList_Size(item),cluster_arr_index)==false){
                free(cluster_arr_index);
                free(indexx);
                for(i=0;i<n;i++){
                    free(obs_arr[i]);
                }
                free(obs_arr);
                for (i=0;i<n;i++){
                    free(cluster_arr[i].cent);
                    free(cluster_arr[i].sum);
                }
                free(cluster_arr) ;
                exit(0);}}
        if(a>1){if(starter3(item, PyList_Size(item), a, obs_arr)==false){
                free(cluster_arr_index);
                free(indexx);
                for(i=0;i<n;i++){
                    free(obs_arr[i]);
                }
                free(obs_arr);
                for (i=0;i<n;i++){
                    free(cluster_arr[i].cent);
                    free(cluster_arr[i].sum);
                }
                free(cluster_arr);
                exit(0);
                }}
    }
    for(i=0;i<k;i++){
        for(j=0;j<d;j++){
            z=(int)cluster_arr_index[i];
            cluster_arr[i].cent[j]=obs_arr[z][j];
        }
    }

    // implementing kmaens algorithem. calculating clusters.
    for(i=0;i<max_iter;i++){
        for(j=0;j<k;j++){
            for(l=0;l<d;l++){
                cluster_arr[j].sum[l] = 0.00;
                cluster_arr[j].size = 0.00;
            }
        }
        for(m=0; m<n; m++){
            c = find_min(obs_arr[m], cluster_arr, k, d);
            if(i==(max_iter-1))
            {
                pp = (long)c;// c is the cluster wich the m observation is assigend to.
                indexx[m] = pp;
            }
            add_to_sum(&cluster_arr[c], obs_arr[m], d);
            cluster_arr[c].size += 1;
        }
        count=0;
        for(m=0; m<k; m++){

            calc_cen(&cluster_arr[m], d);
        }
    }
    torett = make_list(indexx, b-2);// turning c array to python list
    for(i=0;i<n;i++){
        free(obs_arr[i]);
    }
    free(obs_arr);
    for(j=0;j<k;j++){
        free(cluster_arr[j].cent);
        free(cluster_arr[j].sum);
    }
    free(cluster_arr);
    return torett;
}

// first initialize
static void starter(PyObject * list, Py_ssize_t list_size, int* k, int* n, int* d, int* max){
    Py_ssize_t i;
    PyObject *item;
    double *my_c_list = malloc(sizeof my_c_list * list_size);
    if(!(my_c_list != NULL && "Problem in starter")){
        printf("problem with initialezation");
        exit(0);}
    for (i = 0; i < list_size; i++) {
        item = PyList_GetItem(list, i);
        my_c_list[i] = PyFloat_AsDouble(item);
        if (my_c_list[i]  == -1 && PyErr_Occurred()){
            puts("Something bad ...");
            free(my_c_list);
            return;
        }
    }
    *k=(int)my_c_list[0];
    *n=(int)my_c_list[1];
    *d=(int)my_c_list[2];
    *max=(int)my_c_list[3];
}

// initializing index array
static bool starter2(PyObject * list, Py_ssize_t list_size, double* indarr){
    Py_ssize_t i;
    PyObject *item;
    double *my_c_list = malloc(sizeof my_c_list * list_size);
    if(!(my_c_list != NULL && "Problem in starter2")){
        printf("problem with initialization");
        return false;}
    for (i = 0; i < list_size; i++) {
        item = PyList_GetItem(list, i);
        my_c_list[i] = PyFloat_AsDouble(item);
        if (my_c_list[i]  == -1 && PyErr_Occurred()){
            puts("Something bad ...");
            free(my_c_list);
            return false;
        }
        indarr[i]=my_c_list[i];
    }
    free(my_c_list);
    return true;
}
// initializing observation array
static bool starter3(PyObject * list, Py_ssize_t list_size, int j, double** obs_arr){
    Py_ssize_t i;
    PyObject *item;
    double *my_c_list = malloc(sizeof my_c_list * list_size);
    if(!(my_c_list != NULL && "Problem in starter3")){
        printf("problem with initialization");
        return false;}
    for (i = 0; i < list_size; i++) {
        item = PyList_GetItem(list, i);
        my_c_list[i] = PyFloat_AsDouble(item);
        if (my_c_list[i]  == -1 && PyErr_Occurred()){
            puts("Something bad ...");
            free(my_c_list);
            return false;
        }
        obs_arr[j-2][i] = my_c_list[i];
    }
    free(my_c_list);
    return true;
}

void add_to_sum(cluster* cluster,double* to_add,int dim){
    int i;
    for(i=0;i<dim;i++){
        cluster->sum[i]+=to_add[i];
    }
}

//calculating the value of a cluster
void calc_cen(cluster* cluster, int dim){
    int i;
    double size1=cluster->size;
    double sum1;
    for(i=0;i<dim;i++){
        sum1=cluster->sum[i];
        cluster->cent[i]=(sum1/size1);
    }
}

// calculating the minimum gap from a given observation to all clusters
int find_min(double* singob, cluster* cluster_arr,int k,int d){
    int i,j, minind;
    double min;
    minind=-2;
    min=-5.00;
    for(i=0;i<k;i++){
        double currgap=0.00;
        for(j=0;j<d;j++){
            currgap+=(((cluster_arr[i].cent[j])-(singob[j]))*((cluster_arr[i].cent[j])-(singob[j])));
        }
        if(min==(-5.00)){
            min=currgap;
            minind=i;
        }
        else if(min>currgap){
            min=currgap;
            minind=i;
        }
    }
    return (minind);
}

int check_eq(double* before,double* after, int d ){
    int counterr,i;
    counterr=0;
    for(i=0;i<d;i++){
        if(before[i]!=after[i]){
            counterr+=1;
        }
    }
    if (counterr==0){
        return 1;
    }
    else{
        return 0;
    }

}

// converting c array to python list
PyObject *make_list(long * array, Py_ssize_t size) {
    PyObject *l;
    l= PyList_New(size);
    Py_ssize_t i;
    for (i = 0; i < size; ++i) {
        PyList_SET_ITEM(l, i, PyLong_FromLong(array[i]));
    }
    return l;
}

// printing clusters if needed
void print_cen(cluster* cluster_arr,int k,int d){
    int i,j;
    double topri;
    for(i=0;i<k;i++){
        for(j=0;j<(d-1);j++){
            topri=cluster_arr[i].cent[j];
            printf("%f,",topri);
        }
        topri=cluster_arr[i].cent[d-1];
        printf("%f\n",topri);
    }
}


// cpython interface
#define FUNC(_flag, _name, _docstring) { #_name, (PyCFunction)_name, _flag, PyDoc_STR(_docstring) }

static PyMethodDef capiMethods[] = {
        {"calkmeans",                   /* the Python method name that will be used */
                (PyCFunction) calkmeans, /* the C-function that implements the Python function and returns static PyObject*  */
                     METH_VARARGS,           /* flags indicating parameters
accepted for this function */
                        PyDoc_STR("k means")}, /*  The docstring for the function */
        {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "mykmeanssp", /* name of module */
        NULL, /* module documentation, may be NULL */
        -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
        capiMethods /* the PyMethodDef array from before containing the methods of the extension */
};

PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}