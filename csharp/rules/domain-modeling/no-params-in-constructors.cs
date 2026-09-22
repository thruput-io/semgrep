namespace Thruput.Semgrep.Tests
{
    public interface IRepository { }

    public class VehicleService
    {
        private readonly IRepository[] _repositories;

        // ruleid: csharp-no-params-in-constructors
        public VehicleService(params IRepository[] repositories)
        {
            _repositories = repositories;
        }
    }

    public class ExplicitVehicleService
    {
        private readonly IRepository _repository;

        // ok: csharp-no-params-in-constructors
        public ExplicitVehicleService(IRepository repository)
        {
            _repository = repository;
        }
    }
}
