#include <iostream>

int main() {
    int score = 0;
    std::cout << "Player score: " << score << "\n";
    
    int tip = 0;
    std::cout << "Enter tip amount: ";
    std::cin >> tip;
    std::cout << "You paid " << tip << " dollars.\n";
    
    double tempf;
    double tempc;
    std::cout << "\nEnter the temperature in Fahrenheit: ";
    std::cin >> tempf;
    tempc = (tempf - 32) / 1.8;
    std::cout << "The temp is " << tempc << " degrees Celsius.\n\n";
    
    double height, weight, bmi;
    std::cout << "Type in your height (m): ";
    std::cin >> height;
    std::cout << "Type in your weight (kg): ";
    std::cin >> weight;
    bmi = weight / (height * 2);
    std::cout << "Your BMI is " << bmi << "\n";
    
    return 0;
}
