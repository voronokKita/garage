// code examples
#include <iostream>

void animal_chat() {
    std::string fav, pet;

    std::cout << "What's your favorite animal?\n";
    std::cin >> fav;

    std::cout << "Do you have a " << fav << " as a pet? y/n\n";
    std::cin >> pet;

    if (pet == "y") {
        std::cout << "How lucky you have a " << fav << " as a pet!\n";
    }
    else {
        std::cout << "That's too bad.\n";
    }
}

int main() {
    animal_chat();
}
