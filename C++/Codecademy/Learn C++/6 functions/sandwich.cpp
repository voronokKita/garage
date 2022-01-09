// code reminders
#include <iostream>

bool morning = true;

std::string make_sandwich() {
    std::string sandwich = "";
    sandwich += "bread\n";
    sandwich += "lettuce leaf\n";
    sandwich += "mayonnaise\n";
    sandwich += "cheese\n";
    if (morning) {
        sandwich += "egg\n";
    }
    sandwich += "bread\n";
    return sandwich;
}

int main() {
    std::cout << "Your sandwich:\n" << make_sandwich();
    return 0;
}
