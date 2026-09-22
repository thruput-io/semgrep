namespace Thruput.Semgrep.Tests
{
    public interface ITokenProvider { }

    public class TokenService
    {
        private readonly ITokenProvider _provider;

        // ruleid: csharp-no-nullable-constructor-defaults
        public TokenService(ITokenProvider? tokenProvider = null)
        {
            _provider = tokenProvider;
        }
    }

    public class DefaultTokenService
    {
        private readonly ITokenProvider _provider;

        // ruleid: csharp-no-nullable-constructor-defaults
        public DefaultTokenService(ITokenProvider? tokenProvider = default)
        {
            _provider = tokenProvider;
        }
    }

    public class ExplicitTokenService
    {
        private readonly ITokenProvider _provider;

        // ok: csharp-no-nullable-constructor-defaults
        public ExplicitTokenService(ITokenProvider tokenProvider)
        {
            _provider = tokenProvider;
        }
    }
}
