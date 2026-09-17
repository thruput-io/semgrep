using System.Threading.Tasks;

public class OrderService
{
    public string GetOrderDetails(Task<string> fetchTask)
    {
        // ruleid: csharp-sync-over-async-deadlock
        var result1 = fetchTask.Result;

        // ruleid: csharp-sync-over-async-deadlock
        var result2 = fetchTask.GetAwaiter().GetResult();

        // ruleid: csharp-sync-over-async-deadlock
        fetchTask.Wait();

        return result1;
    }

    public async Task<string> GetOrderDetailsAsync(Task<string> fetchTask)
    {
        // ok: csharp-sync-over-async-deadlock
        var result = await fetchTask;
        return result;
    }
}
