using FileMoving.Services.Interfaces;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace FileMoving.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UploadController : ControllerBase
    {
        private readonly IFileSavingService _fileSavingService;

        public UploadController(IFileSavingService fileSavingService)
        {
            _fileSavingService = fileSavingService;
        }

        [HttpPost, DisableRequestSizeLimit]
        public async Task<IActionResult> UploadAsync()
        {
            try
            {
                IFormFile file = Request.Form.Files.FirstOrDefault();

                if (file != null && file.Length > 0)
                {
                    await _fileSavingService.Save(file);

                    return Ok();
                }
                else
                {
                    return BadRequest();
                }
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex}");
            }
        }
    }
}
