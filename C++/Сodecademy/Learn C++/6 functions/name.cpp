#include <iostream>

void name_x_times(std::string name, int x) {
    while(x > 0) {
        std::cout << name << '\n';
        x--;
    }
}

int main() {
    srand(time(NULL));
    std::string my_name = "Anonim";
    int some_number = rand() % 10;
    name_x_times(my_name, some_number);
}
