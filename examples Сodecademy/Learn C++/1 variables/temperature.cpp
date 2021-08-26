#include <iostream>

int main() {
    double tempf;
    double tempc;
    std::cout << "Enter the temperature in Fahrenheit: ";
    std::cin >> tempf;
    tempc = (tempf - 32) / 1.8;
    std::cout << "The temp is " << tempc << " degrees Celsius.\n";
}
