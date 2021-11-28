using System;

namespace OutParameters
{
  class Program
  {
    static void Main(string[] args)
    {
      string ageAsString = "102";
      bool outcome = Int32.TryParse(ageAsString, out int ageAsInt);
      Console.WriteLine(outcome);
      Console.WriteLine(ageAsInt);

      string nameAsString = "Granny";
      bool outcome2 = Int32.TryParse(nameAsString, out int nameAsInt);
      Console.WriteLine(outcome2);
      Console.WriteLine(nameAsInt);
      
      string statement = "GARRRR";
      statement = Whisper(statement, out bool marker);
      Console.WriteLine(statement);
      Console.WriteLine(marker);
    }
    
    static string Whisper(string phrase, out bool wasWhisperCalled)
    {
      wasWhisperCalled = true;
      return phrase.ToLower();
    }
  }
}
