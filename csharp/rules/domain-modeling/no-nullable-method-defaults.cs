using System.Threading;
using System.Threading.Tasks;

namespace Thruput.Semgrep.Tests
{
    public interface IUserService
    {
        // ruleid: csharp-no-nullable-method-defaults
        void FindUser(string id, string format = null);

        // ruleid: csharp-no-nullable-method-defaults
        void QueryUser(string id, string options = default);

        // ok: csharp-no-nullable-method-defaults
        void GetUser(string id);

        // ok: csharp-no-nullable-method-defaults
        Task<string> GetUserAsync(string id, CancellationToken cancellationToken = default);
    }

    public class UserService : IUserService
    {
        // ruleid: csharp-no-nullable-method-defaults
        public void FindUser(string id, string format = null)
        {
        }

        // ruleid: csharp-no-nullable-method-defaults
        public void QueryUser(string id, string options = default)
        {
        }

        // ruleid: csharp-no-nullable-method-defaults
        public string LookupUser(string id, string metadata = null) => id;

        // ruleid: csharp-no-nullable-method-defaults
        public string SearchUser(string id, string query = default) => id;

        // ok: csharp-no-nullable-method-defaults
        public void GetUser(string id)
        {
        }

        // ok: csharp-no-nullable-method-defaults
        public Task<string> GetUserAsync(string id, CancellationToken cancellationToken = default)
        {
            return Task.FromResult(id);
        }

        // ok: csharp-no-nullable-method-defaults
        public Task<string> FetchUserAsync(string id, CancellationToken cancellationToken = default) => Task.FromResult(id);

        // ok: csharp-no-nullable-method-defaults
        public void ConfigureTimeout(int timeoutSeconds = 30)
        {
        }
    }

    public class BaseHandler
    {
        // ruleid: csharp-no-nullable-method-defaults
        public virtual void Handle(string message, string tag = null)
        {
        }
    }

    public class DerivedHandler : BaseHandler
    {
        // ok: csharp-no-nullable-method-defaults
        public override void Handle(string message, string tag = null)
        {
        }
    }
}
