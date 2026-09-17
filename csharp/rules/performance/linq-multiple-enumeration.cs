using System.Collections.Generic;
using System.Linq;

public class SequenceProcessor
{
    public void ProcessItems(IEnumerable<string> items)
    {
        // ruleid: csharp-linq-multiple-enumeration
        if (items.Any())
        {
            foreach (var item in items)
            {
                System.Console.WriteLine(item);
            }
        }

        // ok: csharp-linq-multiple-enumeration
        var list = items.ToList();
        if (list.Any())
        {
            foreach (var item in list)
            {
                System.Console.WriteLine(item);
            }
        }
    }
}
