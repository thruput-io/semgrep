using Xunit;

public class TestClass
{
    // ruleid: csharp-no-skipped-or-ignored-tests
    [Fact(Skip = "Temporarily disabled")]
    public void SkippedFact()
    {
        Assert.True(true);
    }

    // ruleid: csharp-no-skipped-or-ignored-tests
    [Theory(Skip = "Fix later")]
    [InlineData(1)]
    public void SkippedTheory(int x)
    {
        Assert.Equal(1, x);
    }

    // ok: csharp-no-skipped-or-ignored-tests
    [Fact]
    public void ActiveTest()
    {
        Assert.True(true);
    }
}
