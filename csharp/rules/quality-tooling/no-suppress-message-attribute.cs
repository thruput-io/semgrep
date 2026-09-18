using System.Diagnostics.CodeAnalysis;

namespace Thruput.Semgrep.Tests
{
    public class SuppressMessageTests
    {
        // ruleid: csharp-no-suppress-message-attribute
        [SuppressMessage("Reliability", "CA2000:Dispose objects before losing scope")]
        public void ProcessWithSuppression()
        {
            var stream = new System.IO.MemoryStream();
        }

        // ruleid: csharp-no-suppress-message-attribute
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Style", "IDE0060:Remove unused parameter")]
        public void UnusedParam(int unused)
        {
        }

        // ok: csharp-no-suppress-message-attribute
        public void CleanMethod()
        {
            using var stream = new System.IO.MemoryStream();
        }
    }
}
