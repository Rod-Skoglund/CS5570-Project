# CS5570-Project
UMKC CS 5570 Project

Project Scope
* Use whatever programming language you like to implement a scheduler for a database
* The transactions will be of the form T1: r(x); w(x); r(y) etc.
* Generate random transactions set by the user eg I want 4 transactions
* Generate operations for those transactions on x number of data items. eg. user selects 3 data items. The order generated will be a total ordering
* The operations will be randomly sent to the scheduler. (each transactions operation order will be obeyed). 
* The application can also be given a proposed order of operations sent to a scheduler for testing.
    * r1(x); w2(y); w1(x); r3(z), etc...
* The scheduler will apply some variation of 2PL
* Some form of deadlock prevention
* Isolation levels enforced.  At the top level fully serializable.  Try to work in the other isolation levels as appropriate.
