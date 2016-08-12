using System;
namespace rpncalc
{

	enum DisplayTypes { dec, ascii, hex, oct, bin }

	class StackValue{
		private decimal val;
		public string comment;
		public DisplayTypes displaytype;
		public decimal Value()
		{
			return val;
		}

		public bool Equals(StackValue obj)
		{
			if (obj == null){
					return false;
			}
			if (this.val == obj.val){
				return true;
			}else{
				return false;
			}
		}
		public override string ToString()
		{
			string result = "";

			switch (this.displaytype)
			{
				case DisplayTypes.dec:
					result += this.val.ToString();
					break;
				case DisplayTypes.ascii:
					result += Convert.ToChar(this.val).ToString();
					break;
				case DisplayTypes.hex:
					result += this.val.ToString("X");
					break;
				case DisplayTypes.oct:
					result += Convert.ToInt32(this.val.ToString(), 8).ToString();
					break;
				case DisplayTypes.bin:
					result += Convert.ToInt32(this.val.ToString(), 2).ToString();
					break;
				default:
					result += this.val.ToString();
					break;
			}

			if (! String.IsNullOrEmpty(this.comment)){
				result += '(' + this.comment + ')';
			}

			return result;
		}

	}

	class Interface
	{
		static void Main()
		{
			Console.WriteLine("Test");
		}
	}

}
