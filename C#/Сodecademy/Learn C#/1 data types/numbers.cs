using System;

namespace BusinessSolution
{
  class Program
  {
    static void Main(string[] args)
    {
      double revenue = 853023.45;
      double expenses = 438374.11;
      double netIncome = revenue - expenses;
      Console.WriteLine(netIncome);

      double fixedCosts = 912849.30;
      double salesPrice = 29.99;
      double variableCostPerUnit = 17.65;

      double breakEvenVolume = fixedCosts / (salesPrice - variableCostPerUnit);
      Console.WriteLine(breakEvenVolume);
    }
  }
}
