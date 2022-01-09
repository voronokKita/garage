// code reminders
#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> last_jedi;

    last_jedi.push_back("Kylo");
    last_jedi.push_back("Rey");
    last_jedi.push_back("Luke");
    last_jedi.push_back("Finn");

    std::cout << last_jedi[0] << " ";
    std::cout << last_jedi[1] << " ";
    std::cout << last_jedi[2] << " ";
    std::cout << last_jedi[3] << " ";
}
