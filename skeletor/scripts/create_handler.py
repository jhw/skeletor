import os, re

TemplateDir="skeletor/templates"

def filter_template(tempnames, tempfrag):
    matches=[]
    for tempname in tempnames:
        if tempfrag in tempname:
            matches.append(tempname)
    if matches==[]:
        raise RuntimeError("no matching templates found")
    if len(matches) > 1:
        raise RuntimeError("multiple matching templates found - %s" % ", ".join(matches))
    return matches[0]

def init_env(appname, dirname):
    testclassname="%sTest" % "".join([tok.capitalize()
                                      for tok in dirname.split("/")])
    indexmodpath=".".join(dirname.split("/")+["index"])
    return {"AppName": appname,
            "BucketKey": "%s_BUCKET" % appname.upper(),
            "TableKey": "%s_BUCKET" % appname.upper(),
            "TestClassName": testclassname,
            "IndexModulePath": indexmodpath}

def dump_handler(tempname, dirname, env, tempdir=TemplateDir):
    for filename in os.listdir("%s/%s" % (tempdir, tempname)):
        body=open("%s/%s/%s" % (tempdir, tempname, filename)).read()
        for expr in re.findall(r'#\{[A-Z](?:[a-z]+[A-Z]+)*[a-zA-Z0-9]*\}', body):
            tempkey=expr[2:-1]
            if tempkey not in env:
                raise RuntimeError("%s not found in env for %s/%s" % (tempkey,
                                                                      dirname,
                                                                      filename))
            body=body.replace(expr, env[tempkey])
        with open("%s/%s" % (dirname, filename), 'w') as f:
            f.write(body)

if __name__=="__main__":
    try:
        tempnames=os.listdir(TemplateDir)
        tempfrag=input("template: ")
        tempname=filter_template(tempnames, tempfrag)
        dirname=input("path: ").replace(".", "/")
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        appname=dirname.split("/")[0]
        env=init_env(appname, dirname)    
        dump_handler(tempname, dirname, env)
    except RuntimeError as error:
        print ("Error: %s" % error)
