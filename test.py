import importlib, inspect, os, re, unittest
        
AppName="demo"

def init_handler(tempname, appname=AppName):
    dirname="/".join([appname]+tempname.split("-"))
    testclassname="%sTest" % "".join([tok.capitalize()
                                      for tok in dirname.split("/")])
    indexmodpath=".".join(dirname.split("/")+["index"])
    env={"BucketKey": "%s_BUCKET" % appname.upper(),
         "TableKey": "%s_BUCKET" % appname.upper(),
         "TestClassName": testclassname,
         "IndexModulePath": indexmodpath}
    for filename in os.listdir("templates/%s" % tempname):
        body=open("templates/%s/%s" % (tempname, filename)).read()
        for expr in re.findall(r'#\{[A-Z](?:[a-z]+[A-Z]+)*[a-zA-Z0-9]*\}', body):
            tempkey=expr[2:-1]
            if tempkey not in env:
                raise RuntimeError("%s not found in env for %s/%s" % (tempkey,
                                                                      dirname,
                                                                      filename))
            body=body.replace(expr, env[tempkey])
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open("%s/%s" % (dirname, filename), 'w') as f:
            f.write(body)

def filter_tests(root):
    tests=[]
    for localroot, dirs, files in os.walk(root):
        for filename in files:
            if filename=="test.py":
                absfilename=os.path.join(localroot, filename)
                modname=absfilename.split(".")[0].replace("/", ".")
                mod=importlib.import_module(modname)
                tests+=[obj for name, obj in inspect.getmembers(mod,
                                                                inspect.isclass)
                        if name.endswith("Test")]
    return tests

def run_tests(tests):
    suite=unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))
    runner=unittest.TextTestRunner()
    result=runner.run(suite)
    if (result.errors!=[] or
        result.failures!=[]):
        raise RuntimeError("/n".join([error[1]
                                      for error in result.errors+result.failures]))
            
if __name__=="__main__":
    try:
        for tempname in os.listdir("templates"):
            init_handler(tempname)
        tests=filter_tests(AppName)
        run_tests(tests)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
