#include <iostream>

using namespace std;

int main()
{
    float *a = new float(10);
    auto b = a;
    cout << a << endl;
    cout << b << endl;
    cout << *a << endl;
    float *c = b;
    cout << *c << endl;
    delete a;
    return 0;
}