public class StringChecks
{
    public bool Validate(string input)
    {
        // ruleid: csharp-empty-string-comparison
        if (input == "")
        {
            return false;
        }

        // ruleid: csharp-empty-string-comparison
        if (input != "")
        {
            return true;
        }

        // ok: csharp-empty-string-comparison
        if (string.IsNullOrEmpty(input))
        {
            return false;
        }

        // ok: csharp-empty-string-comparison
        if (string.IsNullOrWhiteSpace(input))
        {
            return false;
        }

        return true;
    }
}
