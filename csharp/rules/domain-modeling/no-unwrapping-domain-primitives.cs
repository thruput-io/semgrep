namespace Thruput.Semgrep.Tests
{
    public class UnwrappingTests
    {
        public bool CompareValues(CustomerId a, CustomerId b)
        {
            // ruleid: csharp-no-unwrapping-domain-primitives
            return a.Value == b.Value;
        }

        public bool CompareIds(Order a, Order b)
        {
            // ruleid: csharp-no-unwrapping-domain-primitives
            return a.Id == b.Id;
        }

        public bool CompareDirectly(CustomerId a, CustomerId b)
        {
            // ok: csharp-no-unwrapping-domain-primitives
            return a == b;
        }

        public bool CompareEquals(Order a, Order b)
        {
            // ok: csharp-no-unwrapping-domain-primitives
            return a.Equals(b);
        }
    }

    public record CustomerId(string Value);
    public record Order(int Id);
}
