from django.shortcuts import render, HttpResponse, redirect
from cmdb import models
import pandas as pd
import datetime
import openpyxl
import json


# Create your views here.
def exwrite(ws, mat):  # 参数1为表，参数2为二维列表
    rowx = len(mat)  # 行
    if rowx == 0:
        ws = ws
    else:
        for i in range(rowx):
            k = i + 1
            colx = len(mat[i])  # 列
            for j in range(colx):
                h = j + 1
                ws.cell(row=k, column=h).value = mat[i][j]
    return ws


def get_excel(path):#打开本地excel并更新数据库
    df = pd.read_excel(path)
    Role_name=df['角色名称']
    Foster_time = df['寄养时间']
    user = df['账号']
    pwd = df['密码']
    District_Service = df['区服']
    type = df['类型']
    Target_boundary = df['目标结界']
    u_id = df['角色id']
    simulator = df['模拟器']
    mode = df['上号方式']
    time1 = df['限制时间']
    time2 = df['到期时间']
    Pit_type = df['坑型']
    # name0=models.UserInfo.objects.values_list('Role_name',flat=True)
    # time0=models.UserInfo.objects.values_list('Foster_time',flat=True)
    # f=open('ef.txt','w+')
    # f.write(name0[2])
    # f.close()
    for i in range(len(Role_name)):
        models.UserInfo.objects.get_or_create(Role_name=Role_name[i], Foster_time=Foster_time[i],user=user[i],
                                      pwd=pwd[i],District_Service=District_Service[i],type=type[i],
                                      Target_boundary=Target_boundary[i],u_id=u_id[i],simulator=simulator[i],
                                      mode=mode[i],time1=time1[i],time2=time2[i],Pit_type=Pit_type[i])


def home(request):
    user_list = models.UserInfo.objects.all()
    return render(request, 'home.html', {'data': user_list})


def get_detail(request):#点击角色名详情
    path = request.path
    name = request.GET['name']
    return HttpResponse(name)


def updata(request):#上传excel更新数据库
    try:
        if request.method == 'POST':
            file_obj = request.FILES.get("myFile")
            with open('static/excel/' + file_obj.name, "wb") as f:
                for line in file_obj:
                    f.write(line)
        get_excel('static/excel/' + file_obj.name)
    except:
        pass
    path = request.path
    path=path.split('updata')[0]###
    return redirect(path+'home/')


def download(request): #下载所有用户列表
    user_list = models.UserInfo.objects.all()
    my_mat=[]
    my_mat.append(['角色名称','寄养时间','账号','密码','区服','类型','目标结界','角色id','模拟器','上号方式','限制时间','到期时间','坑型'])
    for i in user_list:
        my_mat.append([i.Role_name,i.Foster_time,i.user,i.pwd,
                       i.District_Service,i.type,i.Target_boundary,i.u_id,i.simulator,i.mode,
                       i.time1,i.time2,i.Pit_type])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws = exwrite(ws, my_mat)
    now_time = datetime.date.today()
    now_time=str(now_time)
    wb.save('static/download/'+now_time+'.xlsx')
    path = request.path
    path = path.split('download')[0]  ###
    return redirect(path+'static/download/'+now_time+'.xlsx')


def add_items(request):##post请求，未测试 /add/?method=post" post=dict
    postBody = request.body
    data = json.loads(postBody)
    user_list=data['user_list']
    models.UserInfo.objects.get_or_create(Role_name=user_list[0], Foster_time=user_list[1], user=user_list[2],
                                          pwd=user_list[3], District_Service=user_list[4], type=user_list[5],
                                          Target_boundary=user_list[6], u_id=user_list[7], simulator=user_list[8],
                                          mode=user_list[9], time1=user_list[10], time2=user_list[11], Pit_type=user_list[12])
    return HttpResponse('OK')


def delete_items(request):#按角色名删除,/delete/?Keyname=杨小葵
    Keyname = request.GET['Keyname']
    models.UserInfo.objects.filter(Role_name=Keyname).delete()
    return HttpResponse('OK')


def modify(request):##post请求，未测试 /modify/?Keyname="Role_name" post=dict
    Keyname = request.GET['Keyname']
    postBody = request.body
    data = json.loads(postBody)
    user=models.UserInfo.objects.filter(Role_name=Keyname)
    user.update(Role_name=data['Role_name'])
    user.update(Foster_time=data['Foster_time'])
    user.update(user=data['user'])
    user.update(pwd=data['pwd'])
    user.update(District_Service=data['District_Service'])
    user.update(type=data['type'])
    user.update(Target_boundary=data['Role_name'])
    user.update(u_id=data['u_id'])
    user.update(simulator=data['simulator'])
    user.update(mode=data['mode'])
    user.update(time1=data['time1'])
    user.update(time2=data['time2'])
    user.update(Pit_type=data['Pit_type'])
    return HttpResponse('OK')


def get_items(request):#单条查询，关键字为角色名
    Keyname = request.GET['Keyname']
    try:
        user_list = models.UserInfo.objects.filter(Role_name=Keyname)
        user = []
        for i in user_list:
            user.append([i.Role_name, i.Foster_time, i.user, i.pwd,
                         i.District_Service, i.type, i.Target_boundary, i.u_id, i.simulator, i.mode,
                         i.time1, i.time2, i.Pit_type])
        data = {'msg': 'OK', 'user_list': user}
    except:
        data={'msg':'No'}
    return HttpResponse(json.dumps(data))