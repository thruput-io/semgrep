using System.Threading;

namespace Thruput.Semgrep.Tests
{
    public class ParameterCountTests
    {
        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public ParameterCountTests(string a, string b, string c, string d, string e)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public int Add(int a, int b)
        {
            return a + b;
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public void BuildPoint(int x, int y, int z)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public void BuildPointAsync(int x, int y, int z, CancellationToken cancellationToken = default)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public int ExpressionThreeWithToken(int a, int b, int c, CancellationToken ct) => a + b + c;

        // ruleid: csharp-max-parameters-warning
        public void CreateUser(string name, string email, int age, string role)
        {
        }

        // ruleid: csharp-max-parameters-warning
        public int ExpressionFour(int a, int b, int c, int d) => a + b + c + d;

        // ruleid: csharp-max-parameters-warning
        public void CreateUserAsync(string name, string email, int age, string role, CancellationToken cancellationToken = default)
        {
        }

        // ruleid: csharp-max-parameters-warning
        public int ExpressionFourWithToken(int a, int b, int c, int d, CancellationToken ct) => a + b + c + d;

        // ruleid: csharp-max-parameters-error
        public void SendNotification(string user, string title, string body, string channel, bool priority)
        {
        }

        // ruleid: csharp-max-parameters-error
        public void SendNotificationAsync(string user, string title, string body, string channel, bool priority, CancellationToken cancellationToken = default)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        [HttpGet("search")]
        public object SearchCustomers(string name, string street, string city, string state, string country)
        {
            return new object();
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public override string ToString()
        {
            return base.ToString();
        }
    }

    public abstract class BaseHandler
    {
        public abstract void HandleFour(string a, string b, string c, string d);
        public abstract void HandleFive(string a, string b, string c, string d, string e);
        public abstract int ExprFour(int a, int b, int c, int d);
        public abstract int ExprFive(int a, int b, int c, int d, int e);
    }

    public class DerivedHandler : BaseHandler
    {
        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public override void HandleFour(string a, string b, string c, string d)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public override void HandleFive(string a, string b, string c, string d, string e)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public override int ExprFour(int a, int b, int c, int d) => a + b + c + d;

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        public override int ExprFive(int a, int b, int c, int d, int e) => a + b + c + d + e;
    }

    public class HttpGetAttribute : System.Attribute
    {
        public HttpGetAttribute(string template) { }
    }
}
