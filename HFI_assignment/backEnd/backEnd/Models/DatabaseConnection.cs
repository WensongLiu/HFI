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
//    public class DatabaseConnection
//    {
//        private DatabaseConnection()
//        {
//        }

//        private string databaseName = string.Empty;
//        public string DatabaseName
//        {
//            get { return databaseName; }
//            set { databaseName = value; }
//        }

//        public string Password { get; set; }
//        private MySqlConnection connection = null;
//        public MySqlConnection Connection
//        {
//            get { return connection; }
//        }

//        private static DatabaseConnection _instance = null;
//        public static DatabaseConnection Instance()
//        {
//            if (_instance == null)
//                _instance = new DatabaseConnection();
//            return _instance;
//        }

//        public bool IsConnect()
//        {
//            if (Connection == null)
//            {
//                if (String.IsNullOrEmpty(databaseName))
//                    return false;
//                string connString = "SERVER=db4hfi.mysql.database.azure.com" + ";" +
//                                    "DATABASE=dataset_hfi;" +
//                                    "UID=Wensong_Liu@db4hfi;" +
//                                    "PASSWORD=712918.Lwslbs;";
//                connection = new MySqlConnection(connString);
//                connection.Open();
//            }

//            return true;
//        }

//        public void Close()
//        {
//            connection.Close();
//        }
//    }
//}
