using Xunit;

public class UserTests
{
    [Fact]
    public void TestWithBranching()
    {
        // ruleid: csharp-no-branching-or-loops-in-tests
        if (true)
        {
            var user = "Alice";
        }

        // ruleid: csharp-no-branching-or-loops-in-tests
        for (int i = 0; i < 3; i++)
        {
            Assert.True(i >= 0);
        }
    }

    [Fact]
    public void TestLinear()
    {
        // ok: csharp-no-branching-or-loops-in-tests
        var user = "Alice";
        Assert.Equal("Alice", user);
    }
}
