using Plugin.Shell.Contracts;
using RestSharp;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RESTPlugin
{
    public class RESTPlugin : IWebServicePlugin
    {
        public string Name
        {
            get 
            { 
                return "REST Plugin"; 
            }
        }

        public void InvokeWebService()
        {
            try
            {
                var client = new RestClient("http://example.com");
                // client.Authenticator = new HttpBasicAuthenticator(username, password);

                var request = new RestRequest("resource/{id}", Method.POST);
                request.AddParameter("name", "value"); // adds to POST or URL querystring based on Method
                request.AddUrlSegment("id", "123"); // replaces matching token in request.Resource

                // easily add HTTP Headers
                request.AddHeader("header", "value");

                // execute the request
                IRestResponse response = client.Execute(request);
                var content = response.Content; // raw content as string
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
    }
}
