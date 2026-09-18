using System;
using System.Collections.Generic;
using System.Linq;

namespace Thruput.Semgrep.Tests
{
    public class CollectionReturnTests
    {
        public List<string> GetNames(bool active)
        {
            if (!active)
            {
                // ruleid: csharp-no-null-collection-return
                return null;
            }
            return new List<string> { "Alice", "Bob" };
        }

        public IEnumerable<int> GetNumbers(bool empty)
        {
            if (empty)
            {
                // ruleid: csharp-no-null-collection-return
                return null;
            }
            return new[] { 1, 2, 3 };
        }

        public string[] GetArray(bool empty)
        {
            if (empty)
            {
                // ruleid: csharp-no-null-collection-return
                return null;
            }
            return new[] { "foo" };
        }

        public List<string> GetNamesSafe(bool active)
        {
            if (!active)
            {
                // ok: csharp-no-null-collection-return
                return new List<string>();
            }
            return new List<string> { "Alice", "Bob" };
        }

        public IEnumerable<int> GetNumbersSafe(bool empty)
        {
            if (empty)
            {
                // ok: csharp-no-null-collection-return
                return Enumerable.Empty<int>();
            }
            return new[] { 1, 2, 3 };
        }

        public string[] GetArraySafe(bool empty)
        {
            if (empty)
            {
                // ok: csharp-no-null-collection-return
                return Array.Empty<string>();
            }
            return new[] { "foo" };
        }
    }
}
