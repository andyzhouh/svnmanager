# _*_ coding:utf-8 _*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,render_to_response
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app01.app01form import *
from app01.app01function import *
from app01 import models
from app01.permission import  check_permission
from app01.svnprojectpermission import check_svnproject_permission
from app01.onlinecodepermission import check_online_permission
import string
import conf

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def login(request):
    #登录功能,允许访问的ip
    # ip_list=['127.0.0.1','1.1.1.1']
    # ip = request.META['REMOTE_ADDR']
    # print"-----------IP--->>:",ip
    # if ip not in ip_list:
    #     #return HttpResponse("404 Not Found")
    #     return render(request,'403.html')
    if request.method == 'POST':
        #根据django自带的用户认证取出数据

        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        #global aaa
        #aaa = request.POST.get("username")

        if user is not None:
            #使用自带认证登录
            user_login(request,user)
            #登录成功返回首页
            username = request.POST.get('username')
            return HttpResponseRedirect('/')
        else:
            #登录失败
            login_err = "Wrong username or password!"
            #返回错误消息
            return render(request, 'login.html', {'login_err':login_err})
    #如果是get
    return render(request, 'login.html')
#退出返回登录页
def logout(request):
    user_logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def index(request):
    if request.method =="POST":
        hostall = models.hosts.objects.all()
        userall = models.UserProfile.objects.all()
        snvsall = models.svns.objects.all()


@login_required(login_url='/login/')
def showhost(request):
    hostall = models.hosts.objects.count()
    svnall = models.svns.objects.count()
    groupall = models.hostgroup.objects.count()
    test = 'test'

    assets = models.cmdb.objects.all()


    if request.method == 'POST':

        search = request.POST.get("search",'null')
        print  request.POST,search
        qset = (
            Q(host_name__icontains = search) |
            Q(host_w_ip__icontains = search) |
            Q(host_w_port__icontains = search) |
            Q(host_n_ip__icontains = search) |
            Q(host_n_port__icontains = search) |
            Q(host_user__icontains = search)
            )
        host_list = models.hosts.objects.filter(qset)
        paginator = Paginator(host_list, 10)
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        host_group = models.hostgroup.objects.all()
        return render(request,'showhost.html',{'hosts':host,'hostgroups':host_group})
    else:
        host_list = models.hosts.objects.all()
        paginator = Paginator(host_list, 10)
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        host_group = models.hostgroup.objects.all()
        return render(request,'showhost.html',{'test':test,'hosts':host,'hostgroups':host_group,"hostall":hostall,'svnall':svnall,'groupall':groupall})




@login_required(login_url='/login/')
@check_permission
def showsvn(request):
    if request.method == "POST":
        search = request.POST.get("search",'null')
        qset = (
            Q(svn_name__icontains = search) |
            Q(svn_user__icontains = search) |
            Q(svn_local__icontains = search) |
            Q(svn_path__icontains = search) )
        svn_list = models.svns.objects.filter(qset)
        paginator = Paginator(svn_list, 10)
        page = 1
        try:
            svn = paginator.page(page)
        except PageNotAnInteger:
            svn = paginator.page(1)
        except EmptyPage:
            svn = paginator.page(paginator.num_pages)
        return render(request,'showsvn.html',{'svns':svn})
    else:
        svn_list = models.svns.objects.all()
        paginator = Paginator(svn_list, 40)
        page = request.GET.get('page')
        try:
            svn = paginator.page(page)
        except PageNotAnInteger:
            svn = paginator.page(1)
        except EmptyPage:
            svn = paginator.page(paginator.num_pages)
        return render(request,'showsvn.html',{'svns':svn})



@login_required(login_url='/login/')
def svnadd(request):
    # return HttpResponse("dadfadfsdfa")
    host123 = models.hosts.objects.all()

    if request.method == "POST":
        print("this is svnadd request======",request)
        svnname = request.POST.get('svnname')
        svnuser = request.POST.get('svnuser')
        svnpass = request.POST.get('svnpass')
        svnpasswd = en_str(svnpass)
        localpath = request.POST.get('localpath')
        svnpath = request.POST.get('svnpath')
        #host = request.POST.get('host')
        host = request.POST.get("host11_id")
        print("host======>::::",host)

        #print("=>:",svnname,svnuser,svnpass,localpath,svnpath,host)
        #print("=>:",svnname,svnuser,svnpass,localpath,svnpath)

        try:
            svns(svn_name=svnname,svn_user=svnuser,svn_pass=svnpasswd,svn_local=localpath,host_id = host,svn_path=svnpath,create_user=request.user).save()
        except:
             result = "Add Svn %s Failed!"%svnname
             return HttpResponse(result)

        logname = time.strftime("%Y-%m-%d")+"-svn.log"
        svnlog = os.path.join(settings.BASE_DIR +'/'+ 'svnlog\\').replace('\\','/') +logname

        if not os.path.exists(svnlog):
            f = open(svnlog,'a')
            f.close()
        out = open(svnlog,'a')
        ss = '|'+str(time.strftime('%Y-%m-%d %H:%M'))+'|'
        aaa = request.user.username
        print("addsvnwebuser:----->",str(aaa))
        result = str(aaa)+ss + "  Create" + "  |  "+ svnname.encode('utf-8')
        print("resultend--->",result)
        out.write(result.replace('|','|'))
        out.write('\n-----------------------------------------------------------------\n')
        out.close()


    return render(request,'addsvn.html',{'hostid11':host123})




        # form = svnform(request.POST)
        # if form.is_valid():
        #     svn_name = form.cleaned_data['svn_name']
        #     svn_user = form.cleaned_data['svn_user']
        #     svn_pass = en_str(settings.SECRET_KEY,str(form.cleaned_data['svn_pass']))
        #     svn_local = form.cleaned_data['svn_local']
        #     svn_path = form.cleaned_data['svn_path']
        #     host = form.cleaned_data['host']
        #
        #     try:
        #         svns(svn_name=svn_name,svn_user=svn_user,svn_pass=svn_pass,svn_local=svn_local,svn_path=svn_path,host=host,create_user=request.user).save()
        #     except:
        #         result = "Add Svn %s Failed!"%svn_name
        #         form = svnform()
        #         return render(request,'addsvn.html',{'form':form,'result':result})
    #return render(request,'addsvn.html',{'hostid11':host123})



@login_required(login_url='/login/')
@check_svnproject_permission
def svnupdate(request,svn_id,u_type):
    svn = svns.objects.get(id =svn_id)
    host = svn.host
    u_type = u_type.encode('utf-8')
    global action
    if u_type == "1":
        cmd = r"svn update %s" %svn.svn_local
        action = u"更新"
        print("1 is cmd:",cmd)
        resp = os.popen(cmd).read()
        print"----------------resp", resp
        resp = str(resp)
    #elif u_type == "2":
    else:
        # version_cmd = r"svn info %s |grep Revision: |awk '{print $2}'" %svn.svn_local
        version_cmd = r"svn info %s | grep '^版本:' |awk {'print $2'}" %svn.svn_local
        action = u"回滚"
        resp1 = os.popen(version_cmd).read()
        print"----------------resp", resp1
        resp1 = str(resp1)
        try:
             #now_version = ordinary_ssh(host=host.host_w_ip,username=host.host_user,password=host.host_pass,port=host.host_w_port,cmd=version_cmd)
            now_version = resp1
        except:
            return HttpResponse("get version fail！")
        print now_version
        restore_version = string.atoi(now_version)-1
        cmd = r"svn up -r %d  %s" %(restore_version,svn.svn_local)
        resp = os.popen(cmd).read()
        print"----------------resp2", resp
        resp = str(resp)
    logname = time.strftime("%Y-%m-%d")+"-svn.log"
    svnlog = os.path.join(settings.BASE_DIR +'/'+ 'svnlog\\').replace('\\','/') +logname
    #svnlog = os.path.join(settings.BASE_DIR,'..\\','svnlog\\').replace('\\','/') +logname
    try:
        #result = verification_ssh(host=host.host_w_ip,username=host.host_user,password=host.host_pass,port=host.host_w_port,root_pwd=host.host_root_pwd,cmd=cmd)
        result = resp
        print("res:"),result
    except Exception as e:
        return HttpResponse(str(e))
    if not os.path.exists(svnlog):
        f = open(svnlog,'a')
        f.close()
    out = open(svnlog,'a')
    svnname = svn.svn_name
    ss = ' '+str(time.strftime('%Y-%m-%d %H:%M'))+' '
    aaa = request.user.username
    print("webuser:----->",str( aaa))
    result = str(aaa)+ss + action.encode(encoding='utf-8') + svnname.encode('utf-8') + " " +result.replace(' ',' ')
    print("resultend--->",result)
    out.write(result.replace(' ',' '))
    out.write('\n-----------------------------------------------------------------\n')
    out.close()
    return render(request,'svnlog.html',{'result':result,'svnname':svnname})

@login_required(login_url='/login/')
def showsvnlog(request):
    cmd = 'ls ./svnlog'
    #cmd = 'find ./svnlog -type f -mtime -1 -exec ls {} \;'
    resp = os.popen(cmd).readlines()
    print"----------------resp", resp
    #resp = str(resp)
    if request.method == 'POST':
        log = request.POST.get('logdate').replace('\r\n','')
        logname = str(log)
    else:
        logname = time.strftime("%Y-%m-%d")+"-svn.log"
    svnlog = os.path.join(settings.BASE_DIR +'/'+ 'svnlog\\').replace('\\','/') +logname
    print("svnlog--->",svnlog)

    try:
        f = open(svnlog)
        result = f.read()
        result = result.replace('\n','<br>')
    except Exception as e:
        return HttpResponse("读取日志失败！<br> %s" %str(e))
    f.close()
    return render(request,'svnlog.html',{'resp':resp,'result':result})


@login_required(login_url='/login/')
def svnedit(request,svn_id):
    #麻烦此功能无用不想写了，没时间。直接用django后台修改就行
    return HttpResponse("你木有权限编辑本条记录！")




@login_required(login_url='/login/')
def group(request):
    grouplist = models.hostgroup.objects.all()
    for group in grouplist:
        global group_host_queryset
        group_host_queryset = group.host.all()
    group_host = list(group_host_queryset)

    # listlen = len(group_host)-1
    #
    # while listlen >=0:
    #     print(group_host[listlen])
    #     listlen -= 1
    a = models.UserProfile.objects.all()
    return render(request,'group.html',{"grouplist":grouplist,"group_host":group_host})





@login_required(login_url='/login/')
def addtogroup(request):
    # if request.method == 'POST':
    # grouptype = request.POST['grouptype']
    # if grouptype == "servergroup":
    host_id = request.POST.get('host.id')
    group_id = request.POST.get('group.id')
    print("===============",host_id,group_id)
    host = models.hosts.objects.get(id=host_id)
    group = models.hostgroup.objects.get(id=group_id)
    try :
        group.host.get(id=host_id)
        result = str(host.host_name)+". Already Exists Server Group  ."+str(group.host_groupname)+".  Add to Server Group Failed!"
    except:
        group.host.add(host)
        group.save()
        result = str(host.host_name)+". add to Server Group ."+str(group.host_groupname)+". Success!"
    return HttpResponse(result,mimetype='application/html')

@login_required(login_url='/login/')
def onlinecode(request):
    ## onconf = conf.configure()
    ## onhost = onconf["readyhost"]
    ## readyhost = list(models.hosts.objects.filter(host_w_ip=onhost))
    ## print(readyhost)
    ## return render(request,"onlinecode.html",{"readyhost":readyhost})


    '''
    底下的for循环用于获取models中的dhost字段，然后用jinja2语法在前端配合join展示出来，如果直接在前端host.dhost是不显示的
    不知道是不是因为多对多的关系，相同的例子参考 group
    修正 貌似for循环 的结果没啥卵用。多了就混乱了、前端还是直接for host in hosts,然后在host.dhhost.all,上次是少了all
    '''
    #rhost_list = models.online.objects.all()

    #print("--rhost_list--",rhost_list)
    #for dhost in rhost_list:
    #    #print(dhost)

    #    dhost_queruset = dhost.dhost.all()
    #    print("===dhost===",dhost_queruset)
    #paginator = Paginator(rhost_list, 40)
    #page = request.GET.get('page')
    #try:
    #    host = paginator.page(page)
    #except PageNotAnInteger:
    #    host = paginator.page(1)
    #except EmptyPage:
    #    host = paginator.page(paginator.num_pages)
    #return render(request,'onlinecode.html',{'hosts':host})

    ## print(rhost)
    ## return render(request,"onlinecode.html",{"rhost":rhost})


    #底下这段代码是新的，上面无法使用搜索功能，搜索时候报错
    #"Related Field got invalid lookup: icontains  TypeError"
    #因为online表dhost是多对多的对应host所以出现的错误
    #如下修改字段后正常  dhost__host_name  注意双下划线

    if request.method =='POST':
        search = request.POST.get("search",'null')
        print("---search--->",search)
        qset = (
            Q(shost__icontains = search) |
            Q(sdir__icontains = search) |
            #Q(dhost__icontains = search) |
            #此行在生产环境search的时候会出现两个search结果，还是注释掉吧，Windows7实验环境没问题，不知道啥问题.暂时就这样吧
            #Q(dhost__host_name__icontains = search) |
            Q(ddir__icontains = search) )
        # svn_list = models.svns.objects.filter(qset)
        rhost_list = models.online.objects.filter(qset)

       # print("---rhost_list-->",rhost_list)
        paginator = Paginator(rhost_list, 25)
        dhost = models.hosts.objects.all()
        page = 1
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        return render(request,'onlinecode.html',{'hosts':host,'dhost':dhost})
    else:


        rhost_list = models.online.objects.all()
        #print("--rhost_list--",rhost_list)
        #for dhost in rhost_list:
            #print(dhost)

         #   dhost_queruset = dhost.dhost.all()
          #  print("===dhost===",dhost_queruset)
        paginator = Paginator(rhost_list, 25)
        dhost = models.hosts.objects.all()
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        return render(request,'onlinecode.html',{'hosts':host,'dhost':dhost})





@login_required(login_url='/login/')
@check_online_permission

def pushonline(request,host_id):
    onlinehost = models.online.objects.get(id=host_id)
    onlinesdir =onlinehost.sdir
    onlinexclude = onlinehost.sexcludedir
    print"onlinesdir---->:",onlinesdir
    #onlinedhost = onlinehost.dhost.all()
    onlinedhost = request.POST.getlist('idhost')
    onlineddir = onlinehost.ddir
    print"onlineddir---->:",onlineddir

    sonlinehost = str(onlinehost)
    print"------sonlinehost----",sonlinehost
    #xxoo = models.hosts.objects.get(host_n_ip=sonlinehost)
    xxoo = models.hosts.objects.get(host_n_ip='10.1.10.10')
    print"-------xxoo------",xxoo
    xuser = xxoo.host_user
    xpwd = xxoo.host_root_pwd
    xport = xxoo.host_n_port
    xrootpwd = xxoo.host_root_pwd
    print("onlinehost--:",sonlinehost,xuser,xpwd,xport,xrootpwd)


    for i in onlinedhost:
        ip = models.hosts.objects.get(host_name=i)
        hostip = ip.host_w_ip
        hostuser = ip.host_user
        hostpasswd = ip.host_pass
        hostprot = ip.host_w_port
        hostrootpwd = ip.host_root_pwd
        print("--->",hostip,hostuser,hostpasswd,hostprot,hostrootpwd)
        # print(hostip)

        #cmd = "rsync -avz -e ssh --delete %s %s@%s:%s"%(onlinesdir,hostuser,hostip,onlineddir)
        cmd = "rsync -av -b --exclude-from='%s' --progress  --rsh='ssh -p4591' %s %s@%s:%s"%(onlinexclude,onlinesdir,hostuser,hostip,onlineddir)
        print"use rsync user:",request.user.username
        print"cmd:",cmd


        
        logname = time.strftime("%Y-%m-%d")+"-svn.log"
        svnlog = os.path.join(settings.BASE_DIR +'/'+ 'svnlog\\').replace('\\','/') +logname
        if not os.path.exists(svnlog):
            f = open(svnlog,'a')
            f.close()
        out = open(svnlog,'a')
        ss = ' '+str(time.strftime('%Y-%m-%d %H:%M'))+' '
        aaa = request.user.username
        result = str(aaa) +' '+ ss+' '+ cmd
        out.write(result)
        out.write('\n-----------------------------------------------------------------\n')
        out.close()

       # result = verification_ssh(host=hostip,username=host.host_user,password=host.host_pass,port=host.host_w_port,root_pwd=host.host_root_pwd,cmd=cmd)
        global resultxx
        try:
            #resultxx = verification_ssh(host=sonlinehost,username='root',password=xrootpwd,port=xport,root_pwd=xrootpwd,cmd=cmd)
            resp = os.popen(cmd).read()
            print"--------------cmd--resp", resp
            resp = str(resp)

            resultxx = resp
            if resultxx==u"":
                resultxx="Error......Update Faile,Please Call admin"
        except:
            resultxx = "Error......请联系管理员"
        # print(cmd)
    print("onlinedhost;",onlinedhost)
    # return render(request,'pushcode.html',{"result":resultxx})
    return HttpResponse(resultxx)


@login_required(login_url='/login/')
@check_permission
def assetslist(request):
    if request.method == 'POST':

        search = request.POST.get("search",'null')
        print  request.POST,search
        qset = (
            Q(name__icontains = search)
            )
        name_list = models.cmdb.objects.filter(qset)
        paginator = Paginator(name_list, 10)
        page = request.GET.get('page')
        try:
            asset_name = paginator.page(page)
        except PageNotAnInteger:
            asset_name = paginator.page(1)
        except EmptyPage:
            asset_name = paginator.page(paginator.num_pages)

        return render(request,'assets.html',{'asset_name':asset_name})
    else:
        name_list = models.cmdb.objects.all()
        paginator = Paginator(name_list, 20)
        page = request.GET.get('page')
        try:
            asset_name = paginator.page(page)
        except PageNotAnInteger:
            asset_name = paginator.page(1)
        except EmptyPage:
            asset_name = paginator.page(paginator.num_pages)
        return render(request,'assets.html',{'asset_name':asset_name})
