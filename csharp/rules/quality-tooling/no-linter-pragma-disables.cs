// ruleid: csharp-no-linter-pragma-disables
#pragma warning disable CS8600

// ruleid: csharp-no-linter-pragma-disables
#pragma warning disable CS8618 // Non-nullable field

public class SafeClass
{
    // ok: csharp-no-linter-pragma-disables
    public int Value { get; init; }
}
