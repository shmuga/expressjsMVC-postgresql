#!/usr/bin/python


import os
import json
import sys
from collections import OrderedDict
from optparse import OptionParser
from subprocess import Popen, PIPE, check_call


def loadPackage(packagePath):
    file = open(packagePath, 'r')
    package = json.load(file, object_pairs_hook=OrderedDict)
    file.close()
    return package


def writePackage(content, packagePath):
    content = json.dumps(content, indent=2)
    file = open(packagePath, 'w')
    file.write(content)
    file.close()


def checkModule(module, packagePath):
    package = loadPackage(packagePath)
    modules = package['dependencies'].keys()
    if module not in modules:
        raise Exception("""
        Module """ + module + """ is not in package's dependencies""")


def getModulesVersions(module):
    cmd = 'npm --loglevel=silent show ' + module + ' versions'
    versions = Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
    versions = [version.strip('\b\n\'" []')
                for version in str(versions).strip('\b\n\'" []').split(',')]
    return versions


def getVersionFields(version):
    fields = version.split('.')
    fields.append('')
    patch = fields[2]
    if '-' in patch:
        fields[3] = patch.split('-')[1]
        fields[2] = patch.split('-')[0]
    return [int(field) for field in fields if field]


def getHighestVersion(module):
    versions = [getVersionFields(version)
                for version in getModulesVersions(module)]
    major = max([version[0] for version in versions])
    minor = max([version[1] for version in versions
                 if version[0] == major])
    patch = max([version[2] for version in versions
                 if version[0] == major and
                    version[1] == minor])
    builds = [version[3] for version in versions
              if len(version) > 3 and
                 version[0] == major and
                 version[1] == minor and
                 version[2] == patch]
    version = '.'.join([str(major), str(minor), str(patch)])
    if builds:
        version += '-' + str(max(builds))
    return version.strip()


def getLatestVersion(module):
    cmd = 'npm --loglevel=silent show ' + module + ' version'
    version = Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
    return str(version).strip('\b\n\'" []')


def setVersion(version):
    cmd = 'npm --loglevel=silent version ' + version
    check_call(cmd, shell=True, stdout=open(os.devnull, 'wb'))
    Popen(cmd, shell=True).wait()


def setHighestVersion(module, packagePath):
    checkModule(module, packagePath)
    package = loadPackage(packagePath)
    version = getHighestVersion(module)
    dependencies = package['dependencies']
    dependencies.__setitem__(module, version)
    package.__setitem__('dependencies', dependencies)
    writePackage(package, packagePath)


def setLatestVersion(module, packagePath):
    checkModule(module, packagePath)
    package = loadPackage(packagePath)
    version = getLatestVersion(module)
    dependencies = package['dependencies']
    dependencies.__setitem__(module, version)
    package.__setitem__('dependencies', dependencies)
    writePackage(package, packagePath)


def showDiffVersions(packagePath):
    count = 0
    package = loadPackage(packagePath)
    if 'dependencies' in package.keys():
        dependencies = package['dependencies']
        for module, version in dependencies.items():
            version = version.strip()
            latestVersion = getLatestVersion(module)
            highestVersion = getHighestVersion(module)
            if version != latestVersion or \
               version != highestVersion or \
               latestVersion != highestVersion:
                print("""
        ------------------------------
        MODULE  : """ + module + """
        VERSION : """ + version + """
        LATEST  : """ + latestVersion + """
        HIGHEST : """ + highestVersion)
                count += 1
        if not count:
            print("""
        All modules versions are specified as highest and latest""")
    else:
        print("""
        Module doesn\'t have dependencies""")


def showModuleVersion(packagePath, message=''):
    print(message + loadPackage(packagePath)['version'])


def showModulesList(packagePath):
    package = loadPackage(packagePath)
    print(' '.join(package['dependencies'].keys()))


def incrementVersion(field, packagePath):
    field = field.upper()
    package = loadPackage(packagePath)
    fields = getVersionFields(package['version'])
    if field == 'MAJOR':
        fields[0] += 1
    if field == 'MINOR':
        fields[1] += 1
    if field == 'PATCH':
        fields[2] += 1
    version = '.'.join([str(f) for f in fields[:3]])
    if field == 'BUILD':
        if len(fields) == 4:
            fields[3] += 1
        else:
            fields.append(0)
    if len(fields) == 4:
        version = version + '-' + str(fields[3])
    package['version'] = version
    writePackage(package, packagePath)


def commitVersion(packagePath):
    sys.stdin = open('/dev/tty')
    issue = raw_input("""
        issue:  """)
    status = raw_input("""
        status: """)
    package = loadPackage(packagePath)
    project = package['name']
    version = package['version']
    message = '#' + issue + ' ' + status + ' Build ' + project + '@' + version
    cmd = 'git commit -am "' + message + '"'
    message = Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
    print("""
        """ + str(message))
    branch = str(Popen('git branch', shell=True, stdout=PIPE).communicate()[0])
    branch = [line.strip('* ') for line in branch.splitlines()
              if '*' in line][0]
    cmd = 'git push --quiet origin ' + branch
    Popen(cmd, shell=True).wait()


def main():
    usage = """
        usage: reversioner  [-H <module> ]
                            [-L <module> ]
                            [-S True     ]
                            [-I True     ]
                            [-V True     ]
                            [-C True     ]
                                            package.json
    """
    parser = OptionParser(usage)
    parser.add_option("-H", "--highest",
                      action="store",
                      default=False,
                      dest="highest",
                      help="Sets the highest version to specified module")
    parser.add_option("-L", "--latest",
                      action="store",
                      default=False,
                      dest="latest",
                      help="Sets the latest version to specified module")
    parser.add_option("-S", "--show",
                      action="store",
                      default=False,
                      dest="show",
                      help="Shows the list of package dependencies")
    parser.add_option("-I", "--increment",
                      action="store",
                      default=False,
                      dest="increment",
                      help="Increments specified field of package's version")
    parser.add_option("-V", "--version",
                      action="store",
                      default=False,
                      dest="version",
                      help="Shows current version of the package")
    parser.add_option("-C", "--commit",
                      action="store",
                      default=False,
                      dest="commit",
                      help="Commits version into git in YouTrack format")

    (options, args) = parser.parse_args()

    if len(args) == 0:
        raise Exception(usage)

    packagePath = args[0]

    if options.show:
        showModulesList(packagePath)
    elif options.highest:
        setHighestVersion(options.highest, packagePath)
    elif options.latest:
        setLatestVersion(options.latest, packagePath)
    elif options.increment:
        message = """
        Package version:
        """
        showModuleVersion(packagePath, message)
        field = raw_input("""
        Increment version field:    major/minor/patch/build
        Set version:                <version>
        """)
        if field in ['major', 'minor', 'patch', 'build']:
            incrementVersion(field, packagePath)
        else:
            setVersion(field)
        message = """
        New version:
        """
        showModuleVersion(packagePath, message)
    elif options.version:
        showModuleVersion(packagePath)
    elif options.commit:
        commitVersion(packagePath)
    else:
        showDiffVersions(packagePath)


if __name__ == '__main__':
    main()
