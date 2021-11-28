#include <iostream>
#include "song.hpp"

int main() {
    Song new_song("Back to Black", "Amy Winehouse");
    std::cout << new_song.get_title();
    std::cout << new_song.get_artist();
    
    new_song.add_title("Electric Relaxation");
    new_song.add_artist("A Tribe Called Quest");
    std::cout << new_song.get_title();
    std::cout << new_song.get_artist();
}
