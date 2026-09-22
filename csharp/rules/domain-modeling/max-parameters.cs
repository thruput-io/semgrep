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

        // ruleid: csharp-max-parameters-warning
        public void BuildPoint(int x, int y, int z)
        {
        }

        // ruleid: csharp-max-parameters-warning
        public int ExpressionThree(int a, int b, int c) => a + b + c;

        // ruleid: csharp-max-parameters-error
        public void CreateUser(string name, string email, int age, string role)
        {
        }

        // ruleid: csharp-max-parameters-error
        public void SendNotification(string user, string title, string body, string channel, bool priority)
        {
        }

        // ok: csharp-max-parameters-warning
        // ok: csharp-max-parameters-error
        [HttpGet("search")]
        public object SearchCustomers(string name, string street, string city, string state, string country)
        {
            return new object();
        }
    }

    public class HttpGetAttribute : System.Attribute
    {
        public HttpGetAttribute(string template) { }
    }
}
