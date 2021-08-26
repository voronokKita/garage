#include <iostream>

int main() {
    int year;
    std::cout << "Year: ";
    std::cin >> year;

    if (year < 1000 or year > 9999) {
        std::cout << "The year must be four-digit number.\n";
    }
    else if (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)) {
        std::cout << year << " is a leap year.\n";
    }
    else {
        std::cout << year << " is not a leap year.\n";
    }  
}
