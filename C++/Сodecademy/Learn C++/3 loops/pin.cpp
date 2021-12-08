// code examples
#include <iostream>

int main() {
    int pin = 0;
    int tries = 0;

    std::cout << "BANK OF CODECADEMY\n";
    std::cout << "Enter your PIN: ";
    std::cin >> pin;

    tries++;
    while (pin != 1234 and tries < 3) {
        std::cout << "Enter your PIN: ";
        std::cin >> pin;
        tries++;
    }
    if (pin == 1234) {
        std::cout << "PIN accepted!\n";
        std::cout << "You now have access.\n"; 
    }
    else {
        std::cout << "Access denied.\n";
    }
}
