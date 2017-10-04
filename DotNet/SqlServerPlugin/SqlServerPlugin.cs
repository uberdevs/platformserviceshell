using Plugin;
using Plugin.Shell.Contracts;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SqlServerPlugin
{
    public class SqlServerPlugin : IDataAccessPlugin
    {
        #region IPlugin Members

        public string Name
        {
            get
            {
                return "SQL Server Plugin";
            }
        }

        public void ConnectToDatabase()
        {
            try
            {
                using (var connection = new SqlConnection("Server=;Initial Catalog=;Persist Security Info=;"))
                {
                    connection.Open();
                    using (var command = new SqlCommand("", connection))
                    {
                        using (var reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {

                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        #endregion
    }

}
