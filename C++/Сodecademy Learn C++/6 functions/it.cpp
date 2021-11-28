#include <iostream>

void it() {
    std::cout << "Hello. IT.\n";
    std::cout << "Have you tried turning it off and on again? y/n\n";
    std::string on_off_attempt;
    std::cin >> on_off_attempt;
}

int main() {
    // Conduct IT support  
    it();

    // Check in with Jenn
    std::cout << "Oh hi Jen!\n";

    // Conduct IT support again...
    it();

    // Check in with Roy
    std::cout << "You stole the stress machine? But that's stealing!\n";

    // Conduct IT support yet again...zzzz...
    it();
}
