using Xunit;

namespace Thruput.Semgrep.Tests
{
    // ruleid: csharp-no-test-case-ordering
    [TestCaseOrderer("MyOrderer", "MyAssembly")]
    public class OrderedTestSuite
    {
        [Fact]
        // ruleid: csharp-no-test-case-ordering
        [TestPriority(1)]
        public void StepOne()
        {
            Assert.True(true);
        }

        [Fact]
        // ruleid: csharp-no-test-case-ordering
        [Order(2)]
        public void StepTwo()
        {
            Assert.True(true);
        }
    }

    public class IndependentTestSuite
    {
        // ok: csharp-no-test-case-ordering
        [Fact]
        public void IndependentTestA()
        {
            Assert.Equal(1, 1);
        }

        // ok: csharp-no-test-case-ordering
        [Fact]
        public void IndependentTestB()
        {
            Assert.Equal(2, 2);
        }
    }

    public class TestPriorityAttribute : System.Attribute
    {
        public TestPriorityAttribute(int priority) { }
    }

    public class OrderAttribute : System.Attribute
    {
        public OrderAttribute(int order) { }
    }
}
