// code examples
#include <iostream>

bool needs_it_support() {
    bool support;
    std::cout << "Hello. IT. Have you tried turning it off and on again? Enter 1 for yes, 0 for no.\n";
    std::cin >> support;
    return support;
}

int main() {
    std::cout << needs_it_support();
}
