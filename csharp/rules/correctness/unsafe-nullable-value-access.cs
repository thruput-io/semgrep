public class NullableExample
{
    public int Process(int? maybeNumber)
    {
        // ruleid: csharp-unsafe-nullable-value-access
        int val = maybeNumber.Value;

        // ok: csharp-unsafe-nullable-value-access
        if (maybeNumber.HasValue)
        {
            int safeVal = maybeNumber.Value;
            return safeVal;
        }

        // ok: csharp-unsafe-nullable-value-access
        if (maybeNumber is not null)
        {
            int safeVal2 = maybeNumber.Value;
            return safeVal2;
        }

        return maybeNumber ?? 0;
    }
}
