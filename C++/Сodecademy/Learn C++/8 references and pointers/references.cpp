// code examples
#include <iostream>

int main() {
      int soda = 99;
      int &pop = soda;
      pop++;
      std::cout << soda << '\n';
      std::cout << pop << '\n';
}
