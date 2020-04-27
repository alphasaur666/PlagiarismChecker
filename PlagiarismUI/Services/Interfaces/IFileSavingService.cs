using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace FileMoving.Services.Interfaces
{
    public interface IFileSavingService
    {
        Task Save(IFormFile file);
    }
}