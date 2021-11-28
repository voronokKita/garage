using System;

namespace IfStatement
{
  class Program
  {
    static void Main(string[] args)
    {
      // laundromat:
      int socks = 3;
      if (socks <= 3) {
        Console.WriteLine("Time to do laundry!");
      }
      
      // lunch:
      int people = 12;
      string weather = "bad";
      if (people <= 10 && weather == "nice") {
        Console.WriteLine("SaladMart");
      } else {
        Console.WriteLine("Soup N Sandwich");
      }
      
      // game:
      int guests = 3;
      if (guests >= 4) {
        Console.WriteLine("Catan");
      } else if (guests >= 1) {
        Console.WriteLine("Innovation");
      } else {
        Console.WriteLine("Solitaire");
      }
    }
  }
}
