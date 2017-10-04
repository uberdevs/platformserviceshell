using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Plugin.Shell.Contracts
{
    public interface IWebServicePlugin
    {
        string Name { get; }
        void InvokeWebService();
    }
}
