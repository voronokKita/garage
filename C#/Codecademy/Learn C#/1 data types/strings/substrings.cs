// code reminders
using System;

namespace NameGrab
{
  class Program
  {
    static void Main(string[] args)
    {
      string name = "Farhad Hesam Abbasi";

      // Get first letter
      int charPosition = name.IndexOf("F");
      char firstLetter = name[charPosition];

      // Get last name
      charPosition = name.IndexOf("A");
      string lastName = name.Substring(charPosition);

      Console.WriteLine($"{firstLetter}.{lastName}");
    }
  }
}
