using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;

public class Utils
{
    public static T SimplygonCast<T>(object from, bool cMemoryOwn = false)
    {
        System.Reflection.MethodInfo CPtrGetter = from.GetType().GetMethod("getCPtr", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static);
        return CPtrGetter == null ? default(T) : (T)System.Activator.CreateInstance
        (
            typeof(T),
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance,
            null,
            new object[] { ((HandleRef)CPtrGetter.Invoke(null, new object[] { from })).Handle, cMemoryOwn },
            null
        );
    }

}
