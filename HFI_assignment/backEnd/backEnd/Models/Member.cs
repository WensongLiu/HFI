using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using MySql.Data.MySqlClient;

namespace backEnd.Models
{
    // You may need to install the Microsoft.AspNetCore.Http.Abstractions package into your project
    public class Member
    {
        private List<Member> _members_admin;
        private List<Member> _members;
        public int memberID { set; get; }
        public string fullName { set; get; }
        public string gender { set; get; }
        public string referralDate { set; get; }
        public string referralSource { set; get; }
        public string clientReferredAs { set; get; }
        public string memberStatus { set; get; }
        public string programSought { set; get; }

        public Member(int memberID, string fullName, string gender, string referralDate, string referralSource, string clientReferredAs, string memberStatus, string programSought)
        {
            this.memberID = memberID;
            this.fullName = fullName;
            this.gender = gender;
            this.referralDate = referralDate;
            this.referralSource = referralSource;
            this.clientReferredAs = clientReferredAs;
            this.memberStatus = memberStatus;
            this.programSought = programSought;
        }

        public Member()
        {
        }

        public List<Member> GetAdminMembers()
        {
            _members_admin = new List<Member>();
            string connString = "SERVER=db4hfi.mysql.database.azure.com" + ";" +
                                "DATABASE=dataset_hfi;" +
                                "UID=Wensong_Liu@db4hfi;" +
                                "PASSWORD=712918.Lwslbs;";
            MySqlConnection connection = new MySqlConnection(connString);

            connection.Open();
            String queryString = "SELECT * FROM admin;";
            var cmd = new MySqlCommand(queryString, connection);
            using (var reader = cmd.ExecuteReader())
            {
                while (reader.Read())
                {
                    _members_admin.Add(new Member()
                    {
                        memberID = Convert.ToInt32(reader["memberID"]),
                        fullName = reader["fullName"].ToString(),
                        gender = reader["gender"].ToString(),
                        referralDate = reader["referralDate"].ToString(),
                        referralSource = reader["referralSource"].ToString(),
                        clientReferredAs = reader["clientReferredAs"].ToString(),
                        memberStatus = reader["memberStatus"].ToString(),
                        programSought = reader["programSought"].ToString()
                    });
                }
            }
            return _members_admin;
        }

        public List<Member> GetMembers()
        {
            _members = new List<Member>();
            string connString = "SERVER=db4hfi.mysql.database.azure.com" + ";" +
                                "DATABASE=dataset_hfi;" +
                                "UID=Wensong_Liu@db4hfi;" +
                                "PASSWORD=712918.Lwslbs;";
            MySqlConnection connection = new MySqlConnection(connString);

            connection.Open();
            String queryString = "SELECT * FROM records;";
            var cmd = new MySqlCommand(queryString, connection);
            using (var reader = cmd.ExecuteReader())
            {
                while (reader.Read())
                {
                    _members.Add(new Member()
                    {
                        memberID = Convert.ToInt32(reader["memberID"]),
                        fullName = reader["fullName"].ToString(),
                        gender = reader["gender"].ToString(),
                        referralDate = reader["referralDate"].ToString(),
                        referralSource = reader["referralSource"].ToString(),
                        clientReferredAs = reader["clientReferredAs"].ToString(),
                        memberStatus = reader["memberStatus"].ToString(),
                        programSought = reader["programSought"].ToString()
                    });
                }
            }
            return _members;
        }
    }
}
