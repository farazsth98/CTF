using System;
using System.Runtime.InteropServices;

namespace Custom
{
	// Token: 0x02000003 RID: 3
	[StructLayout(LayoutKind.Explicit)]
	public struct Customer
	{
		// Token: 0x04000003 RID: 3
		[FieldOffset(0)]
		public string CustomerName;

		// Token: 0x04000004 RID: 4
		[FieldOffset(0)]
		public CustomerInfo CustomerInfo;
	}
}
