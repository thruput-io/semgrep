public class NullChecks
{
    public bool Check(object obj)
    {
        // ruleid: csharp-compare-null-equality
        if (obj == null)
        {
            return false;
        }

        // ruleid: csharp-compare-null-equality
        if (obj != null)
        {
            return true;
        }

        // ruleid: csharp-compare-null-equality
        if (null == obj)
        {
            return false;
        }

        // ok: csharp-compare-null-equality
        if (obj is null)
        {
            return false;
        }

        // ok: csharp-compare-null-equality
        if (obj is not null)
        {
            return true;
        }

        return true;
    }
}
