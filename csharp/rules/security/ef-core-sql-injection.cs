public class UserRepository
{
    public void QueryUsers(AppDbContext context, string userInput)
    {
        // ruleid: csharp-ef-core-sql-injection
        var users1 = context.Users.FromSqlRaw($"SELECT * FROM Users WHERE Name = '{userInput}'");

        // ruleid: csharp-ef-core-sql-injection
        var users2 = context.Users.FromSqlRaw(string.Format("SELECT * FROM Users WHERE Name = '{0}'", userInput));

        // ruleid: csharp-ef-core-sql-injection
        context.Database.ExecuteSqlRaw($"UPDATE Users SET Active = 1 WHERE Name = '{userInput}'");

        // ok: csharp-ef-core-sql-injection
        var safeUsers1 = context.Users.FromSqlInterpolated($"SELECT * FROM Users WHERE Name = {userInput}");

        // ok: csharp-ef-core-sql-injection
        var safeUsers2 = context.Users.FromSqlRaw("SELECT * FROM Users WHERE Name = {0}", userInput);
    }
}
