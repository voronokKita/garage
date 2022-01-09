// code reminders
#include <iostream>
#include <algorithm>

bool is_palindrome(std::string text) {
    std::string text2(text);
    reverse(text2.begin(), text2.end());
    return text == text2;
}

int main() {
    std::cout << is_palindrome("madam") << "\n";
    std::cout << is_palindrome("ada") << "\n";
    std::cout << is_palindrome("lovelace") << "\n";
}
