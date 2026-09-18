using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text.Json;

public class SerializationService
{
    public object DeserializePayload(Stream stream, BinaryFormatter formatter)
    {
        // ruleid: csharp-insecure-binary-formatter
        var obj1 = formatter.Deserialize(stream);

        // ruleid: csharp-insecure-binary-formatter
        var obj2 = new BinaryFormatter().Deserialize(stream);

        // ok: csharp-insecure-binary-formatter
        var safeObj = JsonSerializer.Deserialize<MyModel>(stream);

        return obj1;
    }
}
