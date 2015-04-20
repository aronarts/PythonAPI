using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using SimplygonSDKCLR;

namespace GeometryExample
{
    class GeometryExample
    {
        static void Main(string[] args)
        {
            String licensePath = @"C:\Users\David\AppData\Local\DonyaLabs\SimplygonSDK\Simplygon_5_license.dat";
            if (!File.Exists(licensePath))
            {
                Console.WriteLine("License file not found");
            }
            string licenseString = File.ReadAllText(licensePath);
            SimplygonSDK.AddSearchPath(@"c:\Program Files\SimplygonSDK");
            int res = SimplygonSDK.Initialize(null, licenseString);
            if (res != 0)
            {
                Console.WriteLine("Simplygon inititialization failed with error: " + res);
                return;
            }
            ISimplygonSDK sdk = SimplygonSDK.GetSDK();
            Console.WriteLine("Simplygon version: " + sdk.GetVersion());
        }
    }
}
