// code examples
#include <iostream>

int main() {
    int num = 0;
    int square = 0;
    while (num <= 9) {
        square = num * num;
        std::cout << num << "  " << square << "\n";
        num++;
    }
}
