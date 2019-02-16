import sqlite3
import sys

class File:
    def __init__(self,_file,_package):
        self.file=_file
        self.package=_package
    def file(self):
        return self.file
    def longname(self):
        return self.package+"/"+self.file
class GData:
    def __init__(self, _sqldb, _entity, _kind, _package=None, _file=None, _class=None):
        self.db = _sqldb
        self.entity = _entity
        self.kind = _kind
        self.package = _package
        self.file_ = _file
        self.class_ = _class
        self.datas = []
    def append(self, data):
        self.datas.append(data)
    def longname(self):
        vv = "%s %s %s" % (self.entity,self.file_, self.entity)
        return vv
    def __eq__(self, other):
        if other == None:
            return False
        return self.entity==other.entity and self.kind==other.kind and self.package==other.package and self.file_==other.file_ and self.class_==other.class_ 
    def __hash__(self):
        return hash((self.entity,self.kind,self.package, self.file_,self.class_))
    def __repr__(self):
        return str((self.entity,self.kind,self.package,self.file_,self.class_))
    def library(self):
        return ""
    def relname(self):
        return self.file_
    def kindname(self):
        return self.kind
    def ref(self,p):
        if self.file:
            ff=self.file
            ss=list(filter(lambda x: x.kind=="File" and x.entity==ff,self.db.gdata))
            if len(ss)>0:
                return ss[0]
        return None
    def file(self):
        return self
    def metric(self, metrics):
        vv={d.metric:d.value for d in self.datas if d.metric in metrics}
        return vv
    def ents(self,p1,p2):
        ss = list(filter(lambda x: x.metric=='CountParams',self.datas))
        return range(int(ss[0].value)) if ss != None and len(ss)>0 else range(0)

class Data:
    def __init__(self, _entity, _kind, _metric, _value, _package=None, _file=None, _class=None):
        self.entity = _entity
        self.kind = _kind
        self.metric = _metric
        self.value = _value
        self.package = _package
        self.file = _file
        self.class_ = _class
    def __repr__(self):
        return str((self.entity,self.kind,self.metric,self.value,self.package,self.file,self.class_))
    def library(self):
        return ""
class SqlDb:
    def __init__(self, file):
        self._file=file
        self.data=[]
        self.gdata=[]
        self._metrics = set()
        conn = sqlite3.connect(file)
        c = conn.cursor()
        c.execute("SELECT package,file,class,method,metric,value FROM method_metrics")
        for r in c.fetchall():
            #self._metrics.add(r[4])
            self.add_metric(Data(r[3],'Routine',r[4],r[5],r[0],r[1],r[2]))
        c.execute("SELECT package,file,class,metric,value FROM class_metrics")
        for r in c.fetchall():
            #self._metrics.add(r[3])
            self.add_metric(Data(r[2],'Class',r[3],r[4],r[0],r[1]))
        c.execute("SELECT package,metric,value FROM package_metrics")
        for r in c.fetchall():
            #self._metrics.add(r[1])
            self.add_metric(Data(r[0],'Package',r[1],r[2]))
        c.execute("SELECT file,metric,value FROM file_metrics")
        for r in c.fetchall():
            self._metrics.add(r[1])
            self.add_metric(Data(r[0],'File',r[1],r[2]))
    def add_metric(self,dt):
        self.data.append(dt)
        gd = GData(self,dt.entity,dt.kind,dt.package,dt.file,dt.class_)
        if not gd in self.gdata:
            self.gdata.append(gd)
        idx = self.gdata.index(gd)
        self.gdata[idx].append(dt)
    def show(self):
        for i in self.data:
            print(i)
    def close(self):
        pass
    def name(self):
        return "jvm"
    def language(self):
        return ["jvm"]
    def metrics(self):
        return self._metrics
    def metric(self, metric_names):
        ret = {}
        for i in metric_names:
            ret[i] = sum([dt.value for dt in self.data if dt.kind=='File' and dt.metric==i])
        return ret
    def ents(self, kind):
        ct = "aaa"
        print(kind)
        if ('function' in kind):
            ct="Routine"
        elif ('class' in kind):
            ct="Class"
        elif ('file' in kind):
            ct="File"
        return [dt for dt in self.gdata if dt.kind==ct]
if __name__=='__main__':
    db = SqlDb(sys.argv[1])
    print ("ok" )
    print(db.gdata)