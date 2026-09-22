using System.Collections.Generic;

namespace Thruput.Semgrep.Tests
{
    // ruleid: csharp-no-dictionary-subclass-data-bags
    public class TokenClaims : Dictionary<string, object>
    {
    }

    // ruleid: csharp-no-dictionary-subclass-data-bags
    public class LegacyClaims : System.Collections.Generic.Dictionary<string, string>
    {
    }

    // ok: csharp-no-dictionary-subclass-data-bags
    public record StronglyTypedTokenClaims(string Subject, string Issuer, long Expiration, IReadOnlyList<string> Roles);

    // ok: csharp-no-dictionary-subclass-data-bags
    public class StandardDomainEntity
    {
        public string EntityId { get; init; }

        public StandardDomainEntity(string entityId)
        {
            EntityId = entityId;
        }
    }
}
