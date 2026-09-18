using System;
using System.Runtime.InteropServices;

namespace Thruput.Semgrep.Tests
{
    public class PlatformCheckTests
    {
        public string GetAppPath()
        {
            // ruleid: csharp-no-speculative-platform-branching
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                return @"C:\App";
            }
            return "/var/app";
        }

        public void CheckModernOS()
        {
            // ruleid: csharp-no-speculative-platform-branching
            if (OperatingSystem.IsWindows())
            {
                Console.WriteLine("Windows");
            }
        }

        public string GetStandardAppPath()
        {
            // ok: csharp-no-speculative-platform-branching
            return "/var/app/data";
        }
    }
}
