using System;
using System.Threading.Tasks;
using Xunit;
using FluentAssertions;
using Shouldly;

namespace Thruput.Semgrep.Tests
{
    public class Lead
    {
        public DateTime? ClosedAt { get; set; }
        public string Name { get; set; }
    }

    public class AssertionTests
    {
        // ruleid: csharp-test-must-have-assertion
        [Fact]
        public void TestWithoutAssertion()
        {
            var service = new CalculatorService();
            service.DoCalculation(10);
        }

        // ruleid: csharp-test-must-have-assertion
        [Fact]
        public async Task TestAsyncWithoutAssertion()
        {
            var service = new CalculatorService();
            await service.DoCalculationAsync(10);
        }

        // ok: csharp-test-must-have-assertion
        [Fact]
        public void TestWithAssertEqual()
        {
            var service = new CalculatorService();
            var result = service.DoCalculation(10);
            Assert.Equal(20, result);
        }

        // ok: csharp-test-must-have-assertion
        [Fact]
        public void TestWithFluentAssertions()
        {
            var service = new CalculatorService();
            var result = service.DoCalculation(10);
            result.Should().Be(20);
        }

        // ok: csharp-test-must-have-assertion
        [Fact]
        public void TestWithShouldBeNullProperty()
        {
            var lead = new Lead { ClosedAt = null, Name = "Test" };
            lead.ClosedAt.ShouldBeNull();
        }

        // ok: csharp-test-must-have-assertion
        [Fact]
        public void TestWithShouldThrow()
        {
            var service = new CalculatorService();
            Should.Throw<ArgumentException>(() => service.DoCalculation(-1));
        }

        // ok: csharp-test-must-have-assertion
        [Fact]
        public async Task TestWithShouldThrowAsync()
        {
            var service = new CalculatorService();
            await Should.ThrowAsync<ArgumentException>(async () => await service.DoCalculationAsync(-1));
        }
    }

    public class CalculatorService
    {
        public int DoCalculation(int x)
        {
            if (x < 0) throw new ArgumentException();
            return x * 2;
        }

        public Task<int> DoCalculationAsync(int x)
        {
            if (x < 0) throw new ArgumentException();
            return Task.FromResult(x * 2);
        }
    }
}
