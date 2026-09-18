public class ShellHelper
{
    public void Run()
    {
        // ruleid: csharp-no-suppressed-shell-exit-codes
        var cmd1 = "dotnet test || true";

        // ruleid: csharp-no-suppressed-shell-exit-codes
        var cmd2 = "cat file.txt 2>/dev/null";

        // ok: csharp-no-suppressed-shell-exit-codes
        var safeCmd = "dotnet test && dotnet build";
    }
}
