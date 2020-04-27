using FileMoving.Controllers;
using FileMoving.Services.Interfaces;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System;
using System.IO;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace FileMoving.Services
{
    public class FileSavingService : IFileSavingService
    {
        private readonly ILogger<UploadController> _logger;
        private readonly IConfiguration _configuration;

        public FileSavingService(ILogger<UploadController> logger, IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
        }

        public async Task Save(IFormFile file)
        {
            try
            {
                string moveLocation = _configuration.GetSection("MoveLocation").Value;
                CreateFolderIfNotExists(moveLocation);

                string fileName = ContentDispositionHeaderValue.Parse(file.ContentDisposition).FileName.Trim('"');
                string fullPath = Path.Combine(moveLocation, fileName);

                await CreateFileFromStreamAsync(fullPath, file);
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message, e.InnerException?.Message);
                throw;
            }

        }

        private static async Task CreateFileFromStreamAsync(string fullPath, IFormFile file)
        {
            await using var stream = new FileStream(fullPath, FileMode.Create);
            await file.CopyToAsync(stream);

            // equivalent with ^^^
            //await using (var stream = new FileStream(fullPath, FileMode.Create))
            //{
            //    await file.CopyToAsync(stream);
            //}
        }

        private static void CreateFolderIfNotExists(string moveLocation)
        {
            if (!Directory.Exists(moveLocation))
            {
                Directory.CreateDirectory(moveLocation);
            }
        }
    }
}
