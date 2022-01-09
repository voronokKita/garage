// code reminders
using System;

namespace StoryTime
{
  class Program
  {
    static void Main(string[] args)
    {
      string beginning = "Once upon a time was there\nan old and lonely tree\n";
      string middle = "By him folks had come and gone\n";
      string end = "And he was still standing still";

      string story = beginning + middle + end;

      Console.WriteLine(story);
    }
  }
}
