using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Text.RegularExpressions;
using System.Threading;
using System.Xml.Linq;
using Microsoft.Extensions.Options;

namespace Thruput.Semgrep.Tests
{
    public class FeatureOptions
    {
        public DeleteAfter DeleteAfter { get; set; }
        public ArchiveAfter ArchiveAfter { get; set; }
    }

    public class PurgeService
    {
        public void Execute(FeatureOptions options, IClock clock)
        {
            // ruleid: csharp-no-unwrap-domain-value
            var deleteCutoffUtc = (clock.GetCurrentInstant() - options.DeleteAfter.Value).ToDateTimeOffset();

            // ok: csharp-no-unwrap-domain-value
            var safeCutoffUtc = options.DeleteAfter.CalculateCutoff(clock.GetCurrentInstant()).ToDateTimeOffset();
        }
    }

    public class ArchiveService
    {
        public void Run(FeatureOptions featureOptions)
        {
            // ruleid: csharp-no-unwrap-domain-value
            TimeSpan archiveAfter = featureOptions.ArchiveAfter.Value;

            // ok: csharp-no-unwrap-domain-value
            ArchiveAfter safeArchive = featureOptions.ArchiveAfter;
        }
    }

    public class UnwrappedValueObjectTests
    {
        private readonly IOptions<FeatureOptions> _options;
        private readonly Lazy<string> _lazy;
        private readonly AsyncLocal<string> _asyncLocal = new();
        private readonly ThreadLocal<int> _threadLocal = new();

        public UnwrappedValueObjectTests(IOptions<FeatureOptions> options, Lazy<string> lazy)
        {
            _options = options;
            _lazy = lazy;

            // ok: csharp-no-unwrap-domain-value
            var optVal = _options.Value;

            // ok: csharp-no-unwrap-domain-value
            var directOpt = options.Value;

            // ok: csharp-no-unwrap-domain-value
            var lazyVal = _lazy.Value;

            // ok: csharp-no-unwrap-domain-value
            var directLazy = lazy.Value;

            // ok: csharp-no-unwrap-domain-value
            var al = _asyncLocal.Value;

            // ok: csharp-no-unwrap-domain-value
            var tl = _threadLocal.Value;
        }

        public void TestFrameworkExclusions(
            Dictionary<string, string> dict,
            ClaimsPrincipal user,
            Regex regex,
            string input,
            XElement element,
            XAttribute attr,
            int? nullableInt)
        {
            foreach (var kvp in dict)
            {
                // ok: csharp-no-unwrap-domain-value
                var v = kvp.Value;
            }

            // ok: csharp-no-unwrap-domain-value
            var firstVal = dict.FirstOrDefault().Value;

            // ok: csharp-no-unwrap-domain-value
            var singleVal = dict.First(x => x.Key == "key").Value;

            // ok: csharp-no-unwrap-domain-value
            var claimVal = user.FindFirst("sub")?.Value;

            // ok: csharp-no-unwrap-domain-value
            var claimVal2 = user.FindFirst(ClaimTypes.Email).Value;

            var match = regex.Match(input);
            if (match.Success)
            {
                // ok: csharp-no-unwrap-domain-value
                var matchVal = match.Value;

                // ok: csharp-no-unwrap-domain-value
                var grpVal = match.Groups[1].Value;

                // ok: csharp-no-unwrap-domain-value
                var capVal = match.Groups[1].Captures[0].Value;
            }

            // ok: csharp-no-unwrap-domain-value
            var elVal = element.Value;

            // ok: csharp-no-unwrap-domain-value
            var attrVal = attr.Value;

            // ok: csharp-no-unwrap-domain-value
            var num = nullableInt.Value;
        }

        public void TestDomainViolations(DeleteAfter deleteAfter, CustomerId customerId)
        {
            // ruleid: csharp-no-unwrap-domain-value
            var unwrappedDelete = deleteAfter.Value;

            // ruleid: csharp-no-unwrap-domain-value
            var unwrappedCustomer = customerId.Value;

            // ruleid: csharp-no-unwrap-domain-value
            TakeRawPrimitive(deleteAfter.Value);

            // ok: csharp-no-unwrap-domain-value
            TakeDomainType(deleteAfter);
        }

        private void TakeRawPrimitive(TimeSpan span) {}
        private void TakeDomainType(DeleteAfter deleteAfter) {}
    }

    public record DeleteAfter(TimeSpan Value)
    {
        public DateTime CalculateCutoff(DateTime now)
        {
            // ok: csharp-no-unwrap-domain-value
            return now - this.Value;
        }

        public override bool Equals(object obj)
        {
            // ok: csharp-no-unwrap-domain-value
            return obj is DeleteAfter other && Value == other.Value;
        }

        public override int GetHashCode()
        {
            // ok: csharp-no-unwrap-domain-value
            return Value.GetHashCode();
        }

        public override string ToString()
        {
            // ok: csharp-no-unwrap-domain-value
            return Value.ToString();
        }
    }

    public record ArchiveAfter(TimeSpan Value);
    public record CustomerId(string Value);

    public interface IClock
    {
        DateTime GetCurrentInstant();
    }
}
