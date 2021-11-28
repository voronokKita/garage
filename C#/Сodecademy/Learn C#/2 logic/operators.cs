using System;

namespace LogicalOperators
{
  class Program
  {
    static void Main(string[] args)
    {
      // Barcelona
      bool city = true;
      bool beach = true;
      bool hiking = false;      
      
      bool yourNeeds = beach && city;
      bool friendNeeds = beach && hiking;
      bool tripDecision = yourNeeds && friendNeeds;
      Console.WriteLine(tripDecision);
    }
  }
}
