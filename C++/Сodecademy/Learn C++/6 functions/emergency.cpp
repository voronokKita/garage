#include <iostream>

void get_emergency_number(std::string emergency_number) {
    std::cout << "Dial " << emergency_number << '\n';
}

int main() {
  std::string old_emergency_number = "999";
  
  std::string new_emergency_number = "0118 999 881 999 119 725 3";
  
  get_emergency_number(new_emergency_number);
}
