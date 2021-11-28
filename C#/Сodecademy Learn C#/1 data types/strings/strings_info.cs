using System;

namespace PasswordCheck
{
  class Program
  {
    static void Main(string[] args)
    {
      string password = "a92301j2add";

      int passwordLength = password.Length;
      int passwordCheck = password.IndexOf("!");

      Console.WriteLine($"The user password is {password}. Its length is {passwordLength} and it receives a {passwordCheck} check.");
    }
  }
}
