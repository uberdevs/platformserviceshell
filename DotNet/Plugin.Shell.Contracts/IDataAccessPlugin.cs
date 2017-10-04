using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Plugin.Shell.Contracts
{
    public interface IDataAccessPlugin
    {
        string Name { get; }
        void ConnectToDatabase();
    }
}
