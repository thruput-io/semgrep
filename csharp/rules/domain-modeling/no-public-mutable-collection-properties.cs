using System.Collections.Generic;

namespace Thruput.Semgrep.Tests
{
    public class OrderAggregate
    {
        // ruleid: csharp-no-public-mutable-collection-properties
        public List<string> Items { get; init; } = new();

        // ruleid: csharp-no-public-mutable-collection-properties
        public Dictionary<string, int> Stock { get; } = new();

        // ok: csharp-no-public-mutable-collection-properties
        public IReadOnlyList<string> SafeItems { get; init; } = new List<string>();

        // ok: csharp-no-public-mutable-collection-properties
        public IReadOnlyDictionary<string, int> SafeStock { get; } = new Dictionary<string, int>();
    }
}
