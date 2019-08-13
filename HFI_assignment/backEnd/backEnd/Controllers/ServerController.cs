using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using backEnd.Models;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net;
using Newtonsoft.Json;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace backEnd.Controllers
{
    public class ServerController : Controller
    {
        private static NLog.Logger logger = NLog.LogManager.GetCurrentClassLogger();

        /*
            This method is used for checking the loginInfo.
            If this member is an admin, then return all records to the front-end;
            If this member is a normal member, return all members in the same source group;
            If this member's login info doesn't match any record, just return a null value.         
        */
        [HttpPost]
        [Route("api/[controller]/login")]
        public IActionResult Login([FromBody]LoginInfo loginInfo)
        {
            String flag;
            Member m = new Member();
            List<Member> _members_admin = m.GetAdminMembers();
            List<Member> _members = m.GetMembers();
            flag = loginInfo.IsAdmin(_members_admin);
            if(flag != null)
            {
                var response = _members;
                string jsonRes = JsonConvert.SerializeObject(response);
                
                var resp = new HttpResponseMessage();
                resp.StatusCode = (System.Net.HttpStatusCode)200;
                resp.ReasonPhrase = flag;
                //resp.Content = new ObjectContent<Member>(jsonRes, myFormatter, "application/some-format");
                //return Request.CreateResponse<List<Member>>(HttpStatusCode.OK, _members);
                //resp.Content = new StringContent(jsonRes, System.Text.Encoding.UTF8, "application/json");
                return Ok(_members);
            }
            else
            {
                flag = loginInfo.IsAMember(_members);
                if(flag != null)
                {
                    var response = new List<Member>();
                    foreach(Member me in _members)
                    {
                        if (me.referralSource == flag)
                        {
                            response.Add(me);
                        }
                        else continue;
                    }
                    string jsonRes = JsonConvert.SerializeObject(response);
                    var resp = new HttpResponseMessage();
                    resp.StatusCode = (System.Net.HttpStatusCode)299;
                    resp.ReasonPhrase = flag;
                    resp.Content = new StringContent(jsonRes, System.Text.Encoding.UTF8, "application/json");
                    return StatusCode(299,response);
                }
            }
            var re = new HttpResponseMessage();
            re.StatusCode = HttpStatusCode.BadRequest;
            return BadRequest();
        }
    }
}
