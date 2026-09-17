using System;

public class FallbackHandler
{
    public string FetchConfig()
    {
        // ruleid: csharp-no-fallback-return-in-except
        try
        {
            return int.Parse("invalid").ToString();
        }
        catch (FormatException ex)
        {
            return "default";
        }
    }

    public string SafeHandler()
    {
        // ok: csharp-no-fallback-return-in-except
        try
        {
            return int.Parse("123").ToString();
        }
        catch (FormatException ex)
        {
            throw new InvalidOperationException("Failed", ex);
        }
    }
}
