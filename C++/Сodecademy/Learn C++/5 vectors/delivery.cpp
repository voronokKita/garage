// code examples
#include <iostream>
#include <vector>
  
int main() {
    std::vector<double> delivery_order;

    delivery_order.push_back(8.99);
    delivery_order.push_back(3.75);
    delivery_order.push_back(0.99);
    delivery_order.push_back(5.99);

    double total = 0.0;

    for (int i = 0; i < delivery_order.size(); i++) {
        total += delivery_order[i];
    }
    std::cout << total << "\n";
}
