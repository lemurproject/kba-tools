import AssemblyKeys._

name := "kba-tools"

version := "0.1"

libraryDependencies += "org.slf4j" % "slf4j-api" % "1.7.2"

libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.7.2"

libraryDependencies += "org.apache.thrift" % "libthrift" % "0.9.0"

libraryDependencies += "net.htmlparser.jericho" % "jericho-html" % "3.3"

// Disabled since we're using the local version
// libraryDependencies += "net.sourceforge.argparse4j" % "argparse4j" % "0.2.2"  withSources ()


// Include only src/main/java in the compile configuration
// unmanagedSourceDirectories in Compile <<= Seq(javaSource in Compile).join

// Include only src/test/java in the test configuration
unmanagedSourceDirectories in Test <<= Seq(javaSource in Test).join

// Enable sbt-assembly
assemblySettings

// Enable Thrift
// thriftSettings

//import com.github.bigtoast.sbtthrift.ThriftPlugin


// seq(ThriftPlugin.thriftSettings: _*)

assembleArtifact in packageScala := true

