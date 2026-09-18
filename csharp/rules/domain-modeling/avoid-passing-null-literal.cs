public class CallService
{
    public void Execute()
    {
        // ruleid: csharp-avoid-passing-null-literal
        ProcessData("key", null);

        // ok: csharp-avoid-passing-null-literal
        ProcessData("key", "valid-value");
    }

    private void ProcessData(string key, string metadata)
    {
    }
}
