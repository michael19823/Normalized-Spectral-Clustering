# Normalized Spectral Clustering
this project implement a version of the normalized spectral clustering algorithm.
it includes generation of data, visualization and implementing a well known clustering algorithm with all of its components, c extentions 
and cpython API.


 The user executes the program with certain arguments using the invoke library.
in the terminal:
 $python setup.py build_ext --inplace ///  build the c extensions
 $python -m invoke run  /// run the progrgram and genrate the data randomly.

 The program will output:

• A file with the resulting clusters from both algorithms- kmeans clusters algorithm and normalized spectral clustering algorithm.
• A file containing the data points that were used.
• A visualization file comparing the resulting clusters of the two algorithms.


