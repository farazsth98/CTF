using System;

namespace Custom
{
	// Token: 0x02000002 RID: 2
	public class CustomerInfo
	{
		// Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		public virtual void ChangeBalance(int balance)
		{
			this.Balance = balance;
		}

		// Token: 0x06000002 RID: 2 RVA: 0x00002059 File Offset: 0x00000259
		public virtual int BuyItem(long price)
		{
			this.Balance -= (int)price;
			return this.Balance;
		}

		// Token: 0x04000001 RID: 1
		public int Id;

		// Token: 0x04000002 RID: 2
		public int Balance;
	}
}
