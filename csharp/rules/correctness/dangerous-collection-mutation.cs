using System.Collections.Generic;
using System.Linq;

public class MutationService
{
    public void CleanList(List<string> items)
    {
        // ruleid: csharp-dangerous-collection-mutation
        foreach (var item in items)
        {
            if (item.StartsWith("_"))
            {
                items.Remove(item);
            }
        }

        // ruleid: csharp-dangerous-collection-mutation
        foreach (var item in items)
        {
            items.Add("extra");
        }

        // ok: csharp-dangerous-collection-mutation
        foreach (var item in items.ToList())
        {
            if (item.StartsWith("_"))
            {
                items.Remove(item);
            }
        }

        // ok: csharp-dangerous-collection-mutation
        items.RemoveAll(i => i.StartsWith("_"));
    }
}
