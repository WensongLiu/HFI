//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Threading.Tasks;
//using Microsoft.AspNetCore.Builder;
//using Microsoft.AspNetCore.Http;
//using MySql.Data.MySqlClient;

//namespace backEnd.Models
//{
//    // You may need to install the Microsoft.AspNetCore.Http.Abstractions package into your project
//    public class MembersManager
//    {
//        List<Member> _members;
//        private static NLog.Logger logger = NLog.LogManager.GetCurrentClassLogger();

//        public MembersManager()
//        {
//            _members = new List<Member>();

//            var dbCon = DatabaseConnection.Instance();
//            dbCon.DatabaseName = "dataset_hfi";
//            if (dbCon.IsConnect())
//            {
//                string query = "SELECT * FROM records";
//                var cmd = new MySqlCommand(query, dbCon.Connection);
//                using (var reader = cmd.ExecuteReader())
//                {
//                    while (reader.Read())
//                    {
//                        _members.Add(new Member()
//                        {
//                            memberID = Convert.ToInt32(reader["memberID"]),
//                            fullName = reader["fullName"].ToString(),
//                            gender = reader["gender"].ToString(),
//                            referralDate = reader["referralDate"].ToString(),
//                            referralSource = reader["referralSource"].ToString(),
//                            clientReferredAs = reader["clientReferredAs"].ToString(),
//                            memberStatus = reader["memberStatus"].ToString(),
//                            programSought = reader["programSought"].ToString()
//                            //userName = reader["userName"].ToString(),
//                            //emailAddress = reader["emailAddress"].ToString(),
//                            //pwd = reader["pwd"].ToString(),
//                            //userID = Convert.ToInt32(reader["userID"]),
//                            //balance = Convert.ToDouble(reader["balance"]),
//                            //shippingAddress = reader["shippingAddress"].ToString(),
//                            //phoneNo = reader["phoneNo"].ToString(),
//                            //zipCode = reader["zipCode"].ToString(),
//                            //country = reader["country"].ToString()
//                        });
//                    }
//                }
//                //dbCon.Close();
//            }
//        }

//        public IEnumerable<Member> GetAll { get { return _members; } }
//    }
//}
