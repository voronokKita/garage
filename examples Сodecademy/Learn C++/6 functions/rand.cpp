#include <iostream>

int main() {
    srand(time(NULL));
    
    int the_amazing_random_number = rand() % 69;
    std::cout << the_amazing_random_number << '\n';
}
