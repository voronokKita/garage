// code examples
using System;

namespace Return
{
  class Program
  {
    static void Main(string[] args)
    {
      Console.WriteLine(DecoratePlanet("Jupiter"));
      Console.WriteLine("Is Pluto really a dwarf...?");
      Console.WriteLine(IsPlutoADwarf());
      Console.WriteLine("Then how many planets are there in the galaxy...?");
      Console.WriteLine(CountThePlanets());
    }

    static string DecoratePlanet(string planet)
    {
      return $"*.*.* Welcome to {planet} *.*.*";
    }
    
    static bool IsPlutoADwarf()
    {
      return true;
    }
    
    static string CountThePlanets()
    {
      return "8 planets, usually";
    }
  }
}
