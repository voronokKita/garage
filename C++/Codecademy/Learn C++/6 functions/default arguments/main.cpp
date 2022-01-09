// code reminders
#include <iostream>
#include "coffee.hpp"

int main() {
    bool milk = true;
    bool sugar = true;
    std::cout << make_coffee();
    std::cout << make_coffee(milk);
    std::cout << make_coffee(milk, sugar);
    std::cout << make_coffee(false, sugar);
}
