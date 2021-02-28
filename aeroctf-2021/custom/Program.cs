using System;
using System.Collections.Generic;
using System.IO;

namespace Custom
{
	// Token: 0x02000004 RID: 4
	public class Program
	{
		// Token: 0x06000004 RID: 4 RVA: 0x00002078 File Offset: 0x00000278
		public static void Main(string[] args)
		{
			File.ReadAllText("flag.txt");
			List<Customer> customers = new List<Customer>();
			Console.WriteLine("[!] hello!");
			for (;;)
			{
				Console.WriteLine("\n1. create customer\n2. change customer name\n3. change customer balance\n4. show customer name\n5. show customer balance\n6. buy an item\n7. exit\n");
				Console.Write("[?] >>> ");
				string input = Console.ReadLine();
				int option;
				if (!int.TryParse(input, out option) || option < 1 || option > 7)
				{
					Console.WriteLine("[-] incorrect option");
				}
				else if (option == 1)
				{
					int id = customers.Count;
					Customer customer = new Customer
					{
						CustomerInfo = new CustomerInfo
						{
							Id = id
						}
					};
					customers.Add(customer);
					Console.WriteLine(string.Format("[+] id = {0}", id));
				}
				else if (option >= 2 && option <= 6)
				{
					Console.Write("[?] customer id: ");
					input = Console.ReadLine();
					int id2;
					if (!int.TryParse(input, out id2) || id2 < 0 || id2 >= customers.Count)
					{
						Console.WriteLine("[-] incorrect id");
					}
					else if (option == 2)
					{
						Console.Write("[?] name: ");
						input = Console.ReadLine();
						customers[id2] = new Customer
						{
							CustomerInfo = customers[id2].CustomerInfo,
							CustomerName = input
						};
					}
					else if (option == 3)
					{
						Console.Write("[?] balance: ");
						input = Console.ReadLine();
						int balance;
						if (!int.TryParse(input, out balance))
						{
							Console.WriteLine("[-] incorrect balance");
						}
						else
						{
							customers[id2].CustomerInfo.ChangeBalance(balance);
						}
					}
					else if (option == 4)
					{
						Console.WriteLine("[+] name = " + customers[id2].CustomerName);
					}
					else if (option == 5)
					{
						Console.WriteLine(string.Format("[+] balance = {0}", customers[id2].CustomerInfo.Balance));
					}
					else if (option == 6)
					{
						Console.Write("[?] item price: ");
						input = Console.ReadLine();
						long price;
						if (!long.TryParse(input, out price))
						{
							Console.WriteLine("[-] incorrect price");
						}
						else
						{
							int result = customers[id2].CustomerInfo.BuyItem(price);
							Console.WriteLine(string.Format("[+] new balance = {0}", result));
						}
					}
				}
				else if (option == 7)
				{
					break;
				}
			}
			Console.WriteLine("[+] bye");
		}
	}
}
