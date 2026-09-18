public class MutableModel
{
    // ruleid: csharp-no-public-setters
    public string Name { get; set; }

    // ruleid: csharp-no-public-setters
    public int Age { set; get; }

    // ok: csharp-no-public-setters
    public string SafeId { get; init; }

    // ok: csharp-no-public-setters
    public string SafeEmail { get; private set; }

    // ok: csharp-no-public-setters
    public string ReadOnlyProp => "fixed";
}
