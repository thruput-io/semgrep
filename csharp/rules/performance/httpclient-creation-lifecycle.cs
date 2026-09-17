using System.Net.Http;
using System.Threading.Tasks;

public class ApiConsumer
{
    private readonly IHttpClientFactory _factory;

    public ApiConsumer(IHttpClientFactory factory)
    {
        _factory = factory;
    }

    public async Task<string> BadFetchAsync()
    {
        // ruleid: csharp-httpclient-creation-lifecycle
        using var client = new HttpClient();
        return await client.GetStringAsync("https://api.example.com");
    }

    public async Task<string> GoodFetchAsync()
    {
        // ok: csharp-httpclient-creation-lifecycle
        var client = _factory.CreateClient();
        return await client.GetStringAsync("https://api.example.com");
    }
}
