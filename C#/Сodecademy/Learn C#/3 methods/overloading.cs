using System;

namespace MethodOverloading
{
  class Program
  {
    static void Main(string[] args)
    {
      NamePets("Laika", "Albert");
      NamePets("Mango", "Puddy", "Bucket");
      NamePets();
    }
    
    static void NamePets(string foo, string bar)
    {
      Console.WriteLine($"Your pets {foo} and {bar} will be joining your voyage across space!");
    }
    
    static void NamePets(string foo, string bar, string baz)
    {
      Console.WriteLine($"Your pets {foo}, {bar}, and {baz} will be joining your voyage across space!");
    }
    
    static void NamePets()
    {
      Console.WriteLine($"Aw, you have no spacefaring pets :(");
    }
  }
}
