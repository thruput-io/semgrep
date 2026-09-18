namespace Thruput.Semgrep.Tests
{
    public class StrongTypingTests
    {
        // ruleid: csharp-ban-dynamic-and-object
        public void ProcessDynamic(dynamic payload)
        {
            var x = payload.Data;
        }

        // ruleid: csharp-ban-dynamic-and-object
        public object GetUntypedData(string key)
        {
            return new object();
        }

        // ok: csharp-ban-dynamic-and-object
        public override bool Equals(object obj)
        {
            return obj is StrongTypingTests;
        }

        // ok: csharp-ban-dynamic-and-object
        public override int GetHashCode()
        {
            return 42;
        }

        // ok: csharp-ban-dynamic-and-object
        public override string ToString()
        {
            return "StrongTypingTests";
        }

        // ok: csharp-ban-dynamic-and-object
        public string GetTypedData(string key)
        {
            return key.Trim();
        }
    }
}
