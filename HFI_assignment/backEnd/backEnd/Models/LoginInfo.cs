using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using MySql.Data.MySqlClient;
using backEnd.Models;

namespace backEnd.Models
{
    // You may need to install the Microsoft.AspNetCore.Http.Abstractions package into your project
    public class LoginInfo
    {
        public int memberID { private set; get; }
        public string fullName { private set; get; }

        public LoginInfo(int memberID, string fullName)
        {
            this.memberID = memberID;
            this.fullName = fullName;
        }

        //public List<Member> CheckLogin()
        //{
            

        //    return new List<Member>();
        //}

        public string IsAdmin(List<Member> list)
        {
            string flag = "admin";
            if (list.Any(o => (o.fullName.Equals(this.fullName) && o.memberID.Equals(this.memberID))))
                return flag;
            else return null;
        }

        public string IsAMember(List<Member> list)
        {
            foreach(Member m in list)
            {
                if(m.fullName.Equals(this.fullName) && m.memberID.Equals(this.memberID))
                {
                    return m.referralSource;
                }
            }
            return null;
        }
    }
}
