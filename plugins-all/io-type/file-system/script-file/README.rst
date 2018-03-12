This is a driver to package setup files on an file system(fs). The class instance itself will contains the content as byte stream instead of having an reference to file path on fs. This class supports the basic ops listed below. As with all other drivers, this can be replaced with any other driver registered under abstract class :class:`AbstractPackageFileDriver`

Ops:
    
    * install
    * uninstall
    * update

Please refer to documentation for more information
