using System;
using System.Threading;
using System.Threading.Tasks;

namespace Thruput.Semgrep.Tests
{
    public interface IUserService
    {
        // ruleid: csharp-no-nullable-parameters
        void FindUser(string id, string? format);

        // ruleid: csharp-no-nullable-parameters
        void QueryUser(string id, string options = default);

        // ruleid: csharp-no-nullable-parameters
        void CountUsers(Nullable<int> maxLimit);

        // ok: csharp-no-nullable-parameters
        void GetUser(string id);

        // ok: csharp-no-nullable-parameters
        Task<string> GetUserAsync(string id, CancellationToken cancellationToken = default);
    }

    public class UserService : IUserService
    {
        // ruleid: csharp-no-nullable-parameters
        public void FindUser(string id, string? format)
        {
        }

        // ruleid: csharp-no-nullable-parameters
        public void QueryUser(string id, string options = default)
        {
        }

        // ruleid: csharp-no-nullable-parameters
        public void CountUsers(Nullable<int> maxLimit)
        {
        }

        // ruleid: csharp-no-nullable-parameters
        public string LookupUser(string id, string metadata = null) => id;

        // ruleid: csharp-no-nullable-parameters
        public string SearchUser(string id, int? limit) => id;

        // ok: csharp-no-nullable-parameters
        public void GetUser(string id)
        {
        }

        // ok: csharp-no-nullable-parameters
        public Task<string> GetUserAsync(string id, CancellationToken cancellationToken = default)
        {
            return Task.FromResult(id);
        }

        // ok: csharp-no-nullable-parameters
        public Task<string> FetchUserAsync(string id, CancellationToken cancellationToken = default) => Task.FromResult(id);

        // ok: csharp-no-nullable-parameters
        public void ConfigureTimeout(int timeoutSeconds = 30)
        {
        }
    }

    public class BaseHandler
    {
        // ruleid: csharp-no-nullable-parameters
        public virtual void Handle(string message, string? tag = null)
        {
        }
    }

    public class DerivedHandler : BaseHandler
    {
        // ok: csharp-no-nullable-parameters
        public override void Handle(string message, string? tag = null)
        {
        }
    }
}
