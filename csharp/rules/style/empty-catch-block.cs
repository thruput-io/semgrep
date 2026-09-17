using System;

public class ErrorHandling
{
    public void Run()
    {
        // ruleid: csharp-empty-catch-block
        try
        {
            int.Parse("not-a-number");
        }
        catch (Exception ex)
        {
        }

        // ruleid: csharp-empty-catch-block
        try
        {
            int.Parse("not-a-number");
        }
        catch
        {
        }

        // ok: csharp-empty-catch-block
        try
        {
            int.Parse("not-a-number");
        }
        catch (FormatException ex)
        {
            Console.WriteLine($"Invalid format: {ex.Message}");
        }
    }
}
