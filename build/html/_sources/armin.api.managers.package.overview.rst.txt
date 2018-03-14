Introduction to Package
=======================

    Concept of package is not of much difference as compared to other applications. Like any application or operating system (os) have packages, package manager (eg. pip, apt, yum, etc) and package source index, Armin also uses `Package` for maintaining its functionality. Package in `Armin` is not limited to one format / template and supports multiple different formats. To know more about it, go through the below provided sections.
    
Components
----------

    A package have the below given components and each one have its dedicated job to work with an given `Package`:

    +---------------------+---------------------------------------------------------------------------+
    | Component Name      |  Details                                                                  |
    +=====================+===========================================================================+
    | Extractor           | This component extracts or explodes package on the file system. Since     |
    |                     | multiple type of packages are supported, so extractor should know how to  |
    |                     | extract content from the package and notify next component to proceed     |
    |                     | further.                                                                  |
    +---------------------+---------------------------------------------------------------------------+
    | Validator           | The component validates the contents of package and compares it wth       |
    |                     | already configured package schemas                                        |
    +---------------------+---------------------------------------------------------------------------+
    | Runtime Locator     | This component search and locates the runtime which will be used by other |
    |                     | components to resolve dependencies, build (if required), install and      |
    |                     | wraps the package so that it can be interfaced to `Armin` and other sub   |
    |                     | -systems.                                                                 |
    +---------------------+---------------------------------------------------------------------------+
    | Dependency Resolver | As the name suggets, this component looks for the dependencies required   |
    |                     | by the current package, build and install same if required                |
    +---------------------+---------------------------------------------------------------------------+
    | Build System        | Builds the package locally if it is not already built. This component will|
    |                     | not be used if package and its dependencies already exist pre-built       |
    +---------------------+---------------------------------------------------------------------------+
    | Installer           | Installs the package as required                                          |
    +---------------------+---------------------------------------------------------------------------+
    | Wrapper             | Exposes an package through common API language making it useable for other|
    |                     | components                                                                |
    +---------------------+---------------------------------------------------------------------------+

.. uml::

    @startuml

    () IExtractor - [Extractor]
    () IValidator - [Validator]
    () IRuntimeLocator - [RuntimeLocator]
    () IDependencyResolver - [DependencyResolver]
    () IBuildSystem - [BuildSystem]
    () IInstaller - [Installer]
    () IWrapper - [APIWrapper]

    () HTTP

    node "Armin" {
    [Armin Runtime]
    [Package Manager]
    [FileSystem Manager]
    [Component Manager]
    [APIPublisher]
    [...]
    }

    database "MetaRepo" {
    frame "Packages" {
    [Package Meta]
    }

    frame "FileSystem" {
    [FileSystem Meta]
    }
    }

    [Extractor] --> [Validator]
    [Validator] --> [RuntimeLocator]
    [RuntimeLocator] ..> [Armin Runtime]
    [RuntimeLocator] --> [DependencyResolver]
    [DependencyResolver] ..> HTTP
    [DependencyResolver] --> [BuildSystem]
    [BuildSystem] --> [Installer]
    [Installer] ..> [FileSystem Manager]
    [FileSystem Manager] ..> [FileSystem Meta]
    [Installer] ..> [Package Manager]
    [Package Manager] ..> [Package Meta]
    [Installer] --> [APIWrapper]
    [APIWrapper] ..> [APIPublisher]

    @enduml
