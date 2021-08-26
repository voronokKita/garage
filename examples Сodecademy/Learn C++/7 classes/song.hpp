#include <string>


class Song {
    std::string title;
    std::string artist;

    public:
        Song(std::string new_title, std::string new_artist);
        ~Song();
    
        void add_title(std::string new_title);
        std::string get_title();
        
        void add_artist(std::string new_artist);
        std::string get_artist();
};
