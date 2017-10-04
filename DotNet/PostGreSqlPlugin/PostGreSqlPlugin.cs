using Plugin;
using Npgsql;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Plugin.Shell.Contracts;

namespace PostGreSqlPlugin
{
    public class PostGreSqlPlugin : IDataAccessPlugin
    {
        #region IPlugin Members

        public string Name
        {
            get
            {
                return "PostGreSql Plugin"; //
            }
        }

        public void ConnectToDatabase()
        {
            try
            {
                using (var connection = new NpgsqlConnection("Host=;Username=;Password=;Database="))
                {
                    connection.Open();
                    using (var command = new NpgsqlCommand("", connection))
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
