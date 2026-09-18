using System.Security.Cryptography;

public class CryptoService
{
    public void ComputeHashes()
    {
        // ruleid: csharp-weak-hashing-md5-sha1
        using var md5 = MD5.Create();

        // ruleid: csharp-weak-hashing-md5-sha1
        using var sha1 = SHA1.Create();

        // ok: csharp-weak-hashing-md5-sha1
        using var sha256 = SHA256.Create();

        // ok: csharp-weak-hashing-md5-sha1
        using var sha512 = SHA512.Create();
    }
}
