#! /usr/bin/env python
# encoding: utf-8
# WARNING! All changes made to this file will be lost!

import sys
if sys.hexversion < 0x020400f0: from sets import Set as set
typos={'feature':'features','sources':'source','targets':'target','include':'includes','export_include':'export_includes','define':'defines','importpath':'includes','installpath':'install_path',}
meths_typos=['__call__','program','shlib','stlib','objects']
from waflib import Logs,Build,Node,Task,TaskGen,ConfigSet,Errors,Utils
import waflib.Tools.ccroot
def check_same_targets(self):
	mp=Utils.defaultdict(list)
	uids={}
	def check_task(tsk):
		if not isinstance(tsk,Task.Task):
			return
		for node in tsk.outputs:
			mp[node].append(tsk)
		try:
			uids[tsk.uid()].append(tsk)
		except:
			uids[tsk.uid()]=[tsk]
	for g in self.groups:
		for tg in g:
			try:
				for tsk in tg.tasks:
					check_task(tsk)
			except AttributeError:
				check_task(tg)
	dupe=False
	for(k,v)in mp.items():
		if len(v)>1:
			dupe=True
			Logs.error('* Node %r is created by more than one task. The task generators are:'%k)
			for x in v:
				Logs.error('  %d. %r'%(1+v.index(x),x.generator))
	if not dupe:
		for(k,v)in uids.items():
			if len(v)>1:
				Logs.error('* Several tasks use the same identifier. Please check the information on\n   http://waf.googlecode.com/svn/docs/apidocs/Task.html#waflib.Task.Task.uid')
				for tsk in v:
					Logs.error('  - object %r (%r) defined in %r'%(tsk.__class__.__name__,tsk,tsk.generator))
def check_invalid_constraints(self):
	feat=set([])
	for x in list(TaskGen.feats.values()):
		feat.union(set(x))
	for(x,y)in TaskGen.task_gen.prec.items():
		feat.add(x)
		feat.union(set(y))
	ext=set([])
	for x in TaskGen.task_gen.mappings.values():
		ext.add(x.__name__)
	invalid=ext&feat
	if invalid:
		Logs.error('The methods %r have invalid annotations:  @extension <-> @feature/@before_method/@after_method'%list(invalid))
	for cls in list(Task.classes.values()):
		for x in('before','after'):
			for y in Utils.to_list(getattr(cls,x,[])):
				if not Task.classes.get(y,None):
					Logs.error('Erroneous order constraint %r=%r on task class %r'%(x,y,cls.__name__))
def replace(m):
	oldcall=getattr(Build.BuildContext,m)
	def call(self,*k,**kw):
		ret=oldcall(self,*k,**kw)
		for x in typos:
			if x in kw:
				err=True
				Logs.error('Fix the typo %r -> %r on %r'%(x,typos[x],ret))
		return ret
	setattr(Build.BuildContext,m,call)
def enhance_lib():
	for m in meths_typos:
		replace(m)
	old_ant_glob=Node.Node.ant_glob
	def ant_glob(self,*k,**kw):
		if k:
			lst=Utils.to_list(k[0])
			for pat in lst:
				if'..'in pat.split('/'):
					Logs.error("In ant_glob pattern %r: '..' means 'two dots', not 'parent directory'"%k[0])
		return old_ant_glob(self,*k,**kw)
	Node.Node.ant_glob=ant_glob
	old=Task.is_before
	def is_before(t1,t2):
		ret=old(t1,t2)
		if ret and old(t2,t1):
			Logs.error('Contradictory order constraints in classes %r %r'%(t1,t2))
		return ret
	Task.is_before=is_before
	def check_err_features(self):
		lst=self.to_list(self.features)
		if'shlib'in lst:
			Logs.error('feature shlib -> cshlib, dshlib or cxxshlib')
		for x in('c','cxx','d','fc'):
			if not x in lst and lst and lst[0]in[x+y for y in('program','shlib','stlib')]:
				Logs.error('%r features is probably missing %r'%(self,x))
	TaskGen.feature('*')(check_err_features)
	def check_err_order(self):
		if not hasattr(self,'rule'):
			for x in('before','after','ext_in','ext_out'):
				if hasattr(self,x):
					Logs.warn('Erroneous order constraint %r on non-rule based task generator %r'%(x,self))
		else:
			for x in('before','after'):
				for y in self.to_list(getattr(self,x,[])):
					if not Task.classes.get(y,None):
						Logs.error('Erroneous order constraint %s=%r on %r'%(x,y,self))
	TaskGen.feature('*')(check_err_order)
	old_compile=Build.BuildContext.compile
	def check_compile(self):
		check_invalid_constraints(self)
		try:
			ret=old_compile(self)
		finally:
			check_same_targets(self)
		return ret
	Build.BuildContext.compile=check_compile
	def getattri(self,name,default=None):
		if name=='append'or name=='add':
			raise Errors.WafError('env.append and env.add do not exist: use env.append_value/env.append_unique')
		elif name=='prepend':
			raise Errors.WafError('env.prepend does not exist: use env.prepend_value')
		if name in self.__slots__:
			return object.__getattr__(self,name,default)
		else:
			return self[name]
	ConfigSet.ConfigSet.__getattr__=getattri
def options(opt):
	enhance_lib()
def configure(conf):
	pass
