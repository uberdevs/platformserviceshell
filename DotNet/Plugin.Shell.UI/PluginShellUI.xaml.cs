using Plugin;
using Plugin.Shell.Contracts;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Plugin.Shell.UI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class PluginShellUI : Window
    {
        Dictionary<string, IDataAccessPlugin> _DataAccessPlugins;
        Dictionary<string, IWebServicePlugin> _WebServicePlugins;

        public PluginShellUI()
        {
            InitializeComponent();

            _DataAccessPlugins = new Dictionary<string, IDataAccessPlugin>();
            _WebServicePlugins = new Dictionary<string, IWebServicePlugin>();
            //ICollection<IPlugin> plugins = PluginLoader.LoadPlugins("Plugins");
            ICollection<IDataAccessPlugin> dataAccessPlugins = GenericPluginLoader<IDataAccessPlugin>.LoadPlugins("DataAccessPlugins");
            ICollection<IWebServicePlugin> webServicePlugins = GenericPluginLoader<IWebServicePlugin>.LoadPlugins("WebServicePlugins");
            
            foreach (var item in dataAccessPlugins)
            {
                _DataAccessPlugins.Add(item.Name, item);

                Button b = new Button();
                b.Content = item.Name;
                b.Click += b_Click;
                PluginGrid.Children.Add(b);
            }

            foreach (var item in webServicePlugins)
            {
                _WebServicePlugins.Add(item.Name, item);

                Button b = new Button();
                b.Content = item.Name;
                b.Click += b_Click;
                PluginGrid.Children.Add(b);
            }
        }

        private void b_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                Button b = sender as Button;
                if (b != null)
                {
                    string key = b.Content.ToString();

                    if (_DataAccessPlugins.ContainsKey(key))
                    {
                        IDataAccessPlugin daPlugin = _DataAccessPlugins[key];
                        daPlugin.ConnectToDatabase();
                    }

                    if (_WebServicePlugins.ContainsKey(key))
                    {
                        IWebServicePlugin wsPlugin = _WebServicePlugins[key];
                        wsPlugin.InvokeWebService();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}
