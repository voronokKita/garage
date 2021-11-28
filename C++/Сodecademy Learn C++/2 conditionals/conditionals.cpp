#include <iostream>
#include <stdlib.h>
#include <ctime>

int main() {
    int grade = 90;
    if (grade > 60) {
        std::cout << "Pass\n";
    }
    else {
        std::cout << "Fail\n";
    }
    
    int hunger = true;
    int anger = true;
    if (hunger == true and anger == true) {
        std::cout << "Hangry\n";
    }
    
    int day = 6;
    if (day == 6 or day == 7) {
        std::cout << "Weekend\n";
    }
    
    bool logged_in = false;
    if (!logged_in) {
        std::cout << "Try again\n";
    }
    
    double ph = 4.6;    
    if (ph > 7) {
        std::cout << "Basic\n";
    }
    else if (ph < 7) {
        std::cout << "Acidic\n";
    }
    else {
        std::cout << "Neutral\n";
    }
    
    srand (time(NULL));
    int	coin = rand() % 2;
    if (coin == 0) {
        std::cout << "Heads\n";
    }
    else {
        std::cout << "Tails\n";
    }
    
    return 0;
}
