// code examples
using System;

namespace CallAMethod
{
  class Program
  {
    static void Main(string[] args)
    {
      string msg = "Yabba dabba doo!";
      Console.WriteLine(msg);
      
      msg.Substring(0, 1);
      
      string designer = "Anders Hejlsberg";
      int indexOfSpace = designer.IndexOf(" ");
      string secondName = designer.Substring(indexOfSpace);
      Console.WriteLine(secondName);
      
      VisitPlanets(Math.Min(1, 10));
      VisitPlanets();
    }
    static void VisitPlanets(int numberOfPlanets = 0)
    {
      Console.WriteLine($"You visited {numberOfPlanets} new planets...");
    }
  }
}
